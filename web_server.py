#!/usr/bin/env python3
"""
Web server for SCO Unix Simulator with xterm.js terminal
Provides browser-based access to the modem simulator
"""

from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import threading
import queue
import sys
from io import StringIO
from modem import ModemSimulator
from shell import Shell
from vfs import VirtualFileSystem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sco-unix-simulator-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

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

    def send_output(self, text):
        """Send output to the web terminal"""
        socketio.emit('output', {'data': text}, room=self.sid)

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
        """Print text character by character (faster for web)"""
        # For web, we'll send the whole text at once but slightly delayed
        import time
        for char in text:
            self.send_output(char)
            if delay > 0:
                time.sleep(delay * 0.1)  # Reduce delay for better web experience

    def run_simulator(self):
        """Run the complete modem simulation"""
        self.running = True

        try:
            # Replace print function in modem simulator
            original_print = __builtins__.print if isinstance(__builtins__, dict) else __builtins__.print
            self.modem.slow_print = self.slow_print

            # Simulate modem dial
            self.modem.simulate_modem_dial(print_func=self.custom_print)

            # Show login screen
            self.modem.show_login_screen(print_func=self.custom_print)

            # Login process
            attempt = 0
            max_attempts = 3

            while attempt < max_attempts:
                self.send_output("\nlogin: ")
                username = self.input_queue.get().strip()

                self.send_output("Password: ")
                password = self.input_queue.get().strip()

                if username in self.modem.users and self.modem.users[username] == password:
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
            self.modem.logout(print_func=self.custom_print)

        except Exception as e:
            self.custom_print(f"\nError: {str(e)}")
        finally:
            self.running = False
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
    sid = session.get('session_id', str(threading.get_ident()))
    session['session_id'] = sid

    # Create new terminal session
    terminal = WebTerminal(sid)
    sessions[sid] = terminal

    # Start simulator in background thread
    thread = threading.Thread(target=terminal.run_simulator)
    thread.daemon = True
    thread.start()

    emit('connected', {'data': 'Connected to SCO Unix Simulator'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    sid = session.get('session_id')
    if sid in sessions:
        sessions[sid].running = False
        del sessions[sid]


@socketio.on('input')
def handle_input(data):
    """Handle input from the web terminal"""
    sid = session.get('session_id')
    if sid in sessions:
        terminal = sessions[sid]
        input_text = data.get('data', '')
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
