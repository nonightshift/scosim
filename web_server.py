#!/usr/bin/env python3
"""
Web server for SCO Unix Simulator with xterm.js terminal
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
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sco-unix-simulator-secret-key'
# Disable WebSocket, use polling only to avoid WSGI errors
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading',
                   logger=True, engineio_logger=True,
                   ping_timeout=60, ping_interval=25,
                   transports=['polling'])

# Store session data per session ID
sessions = {}


class WebTerminal:
    """Handles terminal I/O for web-based terminal"""

    def __init__(self, sid):
        self.sid = sid
        self.input_queue = queue.Queue()
        self.vfs = VirtualFileSystem()
        self.modem = ModemSimulator()
        self.shell = None
        self.username = None
        self.running = False
        logging.info(f"WebTerminal created for session {sid}")

    def send_output(self, text):
        """Send output to the web terminal"""
        logging.debug(f"[{self.sid[:8]}] Sending output: {repr(text[:50])}")
        try:
            # Use broadcast instead of room to ensure delivery
            socketio.emit('output', {'data': text}, to=self.sid)
            logging.debug(f"[{self.sid[:8]}] Output emitted successfully")
        except Exception as e:
            logging.error(f"[{self.sid[:8]}] Failed to send output: {e}", exc_info=True)

    def read_input(self, prompt=''):
        """Read input from web terminal"""
        if prompt:
            self.send_output(prompt)
        # Wait for input from the queue
        return self.input_queue.get()

    def custom_print(self, text='', end='\n'):
        """Custom print function for web terminal"""
        output = str(text) + end
        self.send_output(output)

    def slow_print(self, text, delay=0.03):
        """Print text with a slight delay for web terminal"""
        # For web, send the whole text at once for better performance
        # xterm.js can handle the full text rendering efficiently
        import time
        if delay > 0:
            time.sleep(delay * 0.5)  # Small delay before sending
        self.send_output(text)

    def run_simulator(self):
        """Run the complete modem simulation"""
        logging.info(f"[{self.sid[:8]}] Starting simulator")
        self.running = True

        try:
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
                self.send_output("\nlogin: ")
                username = self.input_queue.get().strip()
                logging.info(f"[{self.sid[:8]}] Received username: {username}")

                self.send_output("Password: ")
                password = self.input_queue.get().strip()
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
    terminal = WebTerminal(sid)
    sessions[sid] = terminal

    # Send immediate test message
    emit('connected', {'data': 'Connected to SCO Unix Simulator'})
    logging.info(f"Sent 'connected' event to {sid}")

    # Send test output to verify connection works
    emit('output', {'data': 'TEST: Socket.IO connection established\r\n'})
    logging.info(f"Sent test output to {sid}")

    # Delay the start of the simulator to ensure the connection is fully established
    def delayed_start():
        import time
        time.sleep(1)  # Wait 1 second for WebSocket upgrade to complete
        logging.info(f"Starting simulator task for {sid} after delay")
        terminal.run_simulator()

    # Use socketio.start_background_task for proper threading with Flask-SocketIO
    logging.info(f"Scheduling simulator task for {sid}")
    socketio.start_background_task(delayed_start)
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
    """Handle input from the web terminal"""
    sid = request.sid
    if sid in sessions:
        terminal = sessions[sid]
        input_text = data.get('data', '')
        logging.debug(f"[{sid[:8]}] Received input: {repr(input_text)}")
        terminal.input_queue.put(input_text)


@socketio.on('resize')
def handle_resize(data):
    """Handle terminal resize events"""
    # Could be used to adjust output formatting
    pass


if __name__ == '__main__':
    print("Starting SCO Unix Simulator Web Server...")
    print("Access the terminal at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
