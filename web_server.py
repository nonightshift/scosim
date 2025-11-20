#!/usr/bin/env python3
"""
Web server for SCO Unix Simulator with minimal custom terminal
Provides browser-based access to the modem simulator
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading
import queue
import sys
import logging
from io import StringIO
from modem import ModemSimulator
from shell import Shell
from vfs import VirtualFileSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sco-unix-simulator-secret-key'
# Enable WebSocket with fallback to polling
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading',
                   logger=False, engineio_logger=False,
                   ping_timeout=60, ping_interval=25)

# Store session data per session ID
sessions = {}

# Global flag for skip dialin mode
skip_dialin_mode = False


class WebTerminal:
    """Handles terminal I/O for web-based terminal with VT100 support"""

    def __init__(self, sid, skip_dialin=False):
        self.sid = sid
        self.input_queue = queue.Queue()
        self.char_queue = queue.Queue()  # Queue for individual characters
        self.input_buffer = ""  # Buffer for line-based input
        self.vfs = VirtualFileSystem()
        self.modem = ModemSimulator()
        self.shell = None
        self.username = None
        self.running = False
        self.echo_enabled = True  # Control local echo
        self.skip_dialin = skip_dialin  # Skip dial-in process
        logging.info(f"WebTerminal created for session {sid} (skip_dialin={skip_dialin})")

    def send_output(self, text):
        """Send output to the web terminal"""
        try:
            socketio.emit('output', {'data': text}, to=self.sid)
        except Exception as e:
            logging.error(f"[{self.sid[:8]}] Failed to send output: {e}", exc_info=True)

    def process_char(self, char):
        """Process a single character input"""
        if char == '\r' or char == '\n':
            # Enter pressed - complete the line
            line = self.input_buffer
            self.input_buffer = ""
            if self.echo_enabled:
                self.send_output('\r\n')
            self.input_queue.put(line)
        elif char == '\x7f' or char == '\x08':
            # Backspace/Delete
            if len(self.input_buffer) > 0:
                self.input_buffer = self.input_buffer[:-1]
                if self.echo_enabled:
                    # Move cursor back, erase character, move cursor back again
                    self.send_output('\x08 \x08')
        elif char == '\x03':
            # Ctrl+C
            self.input_buffer = ""
            if self.echo_enabled:
                self.send_output('^C\r\n')
            self.input_queue.put('')
        elif char == '\x04':
            # Ctrl+D
            if len(self.input_buffer) == 0:
                self.input_queue.put('exit')
            else:
                # Send partial line
                line = self.input_buffer
                self.input_buffer = ""
                self.input_queue.put(line)
        elif len(char) == 1 and ord(char) >= 32 and ord(char) < 127:
            # Printable character
            self.input_buffer += char
            if self.echo_enabled:
                self.send_output(char)

    def read_input(self, prompt=''):
        """Read input from web terminal (line-based)"""
        if prompt:
            self.send_output(prompt)
        # Wait for input from the queue
        return self.input_queue.get()

    def custom_print(self, text='', end='\n'):
        """Custom print function for VT100 terminal"""
        # Convert \n to \r\n for proper VT100 terminal behavior
        output = str(text) + end
        output = output.replace('\n', '\r\n')
        self.send_output(output)

    def slow_print(self, text, delay=0.03):
        """Print text with a slight delay for VT100 terminal"""
        # For web, send the whole text at once for better performance
        # The VT100 terminal can handle the full text rendering efficiently
        import time
        if delay > 0:
            time.sleep(delay * 0.5)  # Small delay before sending
        # Convert \n to \r\n for proper VT100 terminal behavior
        output = text.replace('\n', '\r\n')
        self.send_output(output)

    def run_simulator(self):
        """Run the complete modem simulation"""
        logging.info(f"[{self.sid[:8]}] Starting simulator")
        self.running = True

        try:
            if self.skip_dialin:
                # Skip dial-in and login directly as root
                logging.info(f"[{self.sid[:8]}] Skipping dial-in, logging in as root")
                self.custom_print("Skipping dial-in process, logging in as root...\r\n")
                self.username = 'root'
                self.modem.show_welcome_message('root', print_func=self.custom_print)

                # Start shell as root
                self.shell = Shell('root', self.vfs)
                self.run_shell()
            else:
                # Normal dial-in process
                # Simulate modem dial
                logging.info(f"[{self.sid[:8]}] Starting modem dial simulation")
                self.modem.simulate_modem_dial(print_func=self.custom_print, slow_print_func=self.slow_print)
                logging.info(f"[{self.sid[:8]}] Modem dial completed")

                # Show login screen
                logging.info(f"[{self.sid[:8]}] Showing login screen")
                self.modem.show_login_screen(print_func=self.custom_print)

                # Login process
                attempt = 0
                max_attempts = 3

                while attempt < max_attempts:
                    logging.info(f"[{self.sid[:8]}] Waiting for login (attempt {attempt + 1})")
                    self.send_output("\r\nlogin: ")
                    username = self.input_queue.get().strip()
                    logging.info(f"[{self.sid[:8]}] Received username: {username}")

                    # Disable echo for password
                    self.echo_enabled = False
                    self.send_output("Password: ")
                    password = self.input_queue.get().strip()
                    # Re-enable echo after password
                    self.echo_enabled = True
                    logging.info(f"[{self.sid[:8]}] Received password")

                    if username in self.modem.users and self.modem.users[username] == password:
                        logging.info(f"[{self.sid[:8]}] Login successful for user: {username}")
                        self.username = username
                        self.modem.show_welcome_message(username, print_func=self.custom_print)

                        # Start shell
                        self.shell = Shell(username, self.vfs)
                        self.run_shell()
                        break
                    else:
                        attempt += 1
                        if attempt < max_attempts:
                            self.custom_print("Login incorrect")

                if attempt >= max_attempts:
                    self.custom_print("\nToo many login failures. Connection terminated.")

                # Logout
                self.modem.logout(print_func=self.custom_print, slow_print_func=self.slow_print)

        except Exception as e:
            logging.error(f"[{self.sid[:8]}] Error in simulator: {str(e)}", exc_info=True)
            self.custom_print(f"\nError: {str(e)}")
        finally:
            self.running = False
            logging.info(f"[{self.sid[:8]}] Simulator ended")
            self.send_output("\r\n\r\n=== Session ended. Refresh page to reconnect. ===\r\n")

    def run_shell(self):
        """Run the interactive shell"""
        while self.running:
            try:
                # Show prompt
                prompt = self.shell.get_prompt()
                self.send_output(prompt)

                # Get command
                command = self.input_queue.get().strip()

                if not command:
                    continue

                # Add to history
                if command and (not self.shell.history or command != self.shell.history[-1]):
                    self.shell.history.append(command)

                # Check for exit
                if command.lower() in ['exit', 'logout']:
                    break

                # Execute command
                self.shell.execute_command(command, print_func=self.custom_print)

            except Exception as e:
                self.custom_print(f"Error: {str(e)}")


@app.route('/')
def index():
    """Serve the main terminal page"""
    return render_template('terminal.html')


@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connection"""
    sid = request.sid
    logging.info(f"New connection: {sid}")
    logging.info(f"Request namespace: {request.namespace}")

    # Create new terminal session
    terminal = WebTerminal(sid, skip_dialin=skip_dialin_mode)
    sessions[sid] = terminal

    # Send connection confirmation
    emit('connected', {'data': 'Connected to SCO Unix Simulator'})
    logging.info(f"Sent 'connected' event to {sid}")

    # Start simulator in background
    def start_simulator():
        import time
        time.sleep(0.1)  # Small delay to ensure connection is ready
        logging.info(f"Starting simulator task for {sid}")
        terminal.run_simulator()

    # Use socketio.start_background_task for proper threading with Flask-SocketIO
    logging.info(f"Scheduling simulator task for {sid}")
    socketio.start_background_task(start_simulator)
    logging.info(f"Simulator task scheduled for {sid}")


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    sid = request.sid
    logging.info(f"Disconnect: {sid}")
    if sid in sessions:
        sessions[sid].running = False
        del sessions[sid]
        logging.info(f"Session {sid} cleaned up")


@socketio.on('input')
def handle_input(data):
    """Handle input from the web terminal (character-by-character)"""
    sid = request.sid
    if sid in sessions:
        terminal = sessions[sid]
        input_text = data.get('data', '')
        # Process each character
        for char in input_text:
            terminal.process_char(char)


@socketio.on('resize')
def handle_resize(data):
    """Handle terminal resize events"""
    # Could be used to adjust output formatting
    pass


if __name__ == '__main__':
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SCO Unix Simulator Web Server')
    parser.add_argument('--skip-dialin', action='store_true',
                       help='Skip dial-in process and login directly as root')
    args = parser.parse_args()

    # Set global skip dialin mode
    skip_dialin_mode = args.skip_dialin

    print("Starting SCO Unix Simulator Web Server...")
    if skip_dialin_mode:
        print("Mode: Skip dial-in (auto-login as root)")
    print("Access the terminal at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
