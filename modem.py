"""
Modem Simulator Module
Implements the modem dial-in and connection simulation
"""

import sys
import time
import random
import getpass
from system_time import now


class ModemSimulator:
    """Simulates a classic modem login experience"""

    def __init__(self):
        self.connected = False
        self.logged_in = False
        self.username = None

        # Default users for demo (in production passwords should be hashed)
        self.users = {
            "root": "root",
            "sysadmin": "admin123",
            "user": "password",
            "guest": "guest"
        }

    def slow_print(self, text, delay=0.05):
        """Prints text character by character for authentic retro effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def print_instant(self, text):
        """Prints text instantly"""
        print(text)

    def simulate_modem_dial(self, print_func=None):
        """Simulates the modem dial-in process"""
        # Use custom print function if provided, otherwise use default
        _print = print_func if print_func else self.print_instant
        _slow_print = self.slow_print

        _print("\n" + "="*60)
        _print("     MODEM COMMUNICATIONS SIMULATOR v2.4")
        _print("     Copyright (C) 1995-1998")
        _print("="*60 + "\n")

        time.sleep(0.5)
        _slow_print("Initializing modem...", 0.03)
        time.sleep(0.3)

        # AT commands
        at_commands = [
            ("AT", "OK"),
            ("ATZ", "OK"),
            ("ATE1", "OK"),
            ("ATM1", "OK"),
            ("ATX4", "OK"),
            ("ATDT 555-1234", "")
        ]

        for cmd, response in at_commands:
            _slow_print(f"{cmd}", 0.02)
            time.sleep(0.2)
            if response:
                _slow_print(response, 0.02)
            time.sleep(0.3)

        # Simulate dialing sounds
        _print("")
        _slow_print("Dialing...", 0.04)
        time.sleep(0.5)

        dial_sounds = ["BEEP", "BEEP", "BEEP", "BEEP", "BEEP", "BEEP", "BEEP"]
        for sound in dial_sounds:
            if print_func:
                print_func(sound + " ", end='')
            else:
                sys.stdout.write(sound + " ")
                sys.stdout.flush()
            time.sleep(0.15)
        _print("\n")

        time.sleep(0.5)
        _slow_print("Connecting...", 0.04)
        time.sleep(0.8)

        # Modem handshake sounds as text
        handshake = [
            "RRRRR.....",
            "KSSSSSHHHHhhhh....",
            "BEEEEeeeeee....",
            "WRRRRrrrrrr....",
            "CHHHhhhhh...."
        ]

        for sound in handshake:
            _slow_print(sound, 0.02)
            time.sleep(0.3)

        time.sleep(0.5)
        _print("")
        _slow_print("CONNECT 14400/V.32bis", 0.03)
        self.connected = True
        time.sleep(0.5)

    def show_login_screen(self, print_func=None):
        """Displays the login screen"""
        _print = print_func if print_func else self.print_instant

        _print("\n" + "="*60)
        _print("")
        _print("     ███████╗ ██████╗ ██████╗     ██╗   ██╗███╗   ██╗██╗██╗  ██╗")
        _print("     ██╔════╝██╔════╝██╔═══██╗    ██║   ██║████╗  ██║██║╚██╗██╔╝")
        _print("     ███████╗██║     ██║   ██║    ██║   ██║██╔██╗ ██║██║ ╚███╔╝ ")
        _print("     ╚════██║██║     ██║   ██║    ██║   ██║██║╚██╗██║██║ ██╔██╗ ")
        _print("     ███████║╚██████╗╚██████╔╝    ╚██████╔╝██║ ╚████║██║██╔╝ ██╗")
        _print("     ╚══════╝ ╚═════╝ ╚═════╝      ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝")
        _print("")
        _print("     SCO UNIX System V/386 Release 3.2")
        _print("     Copyright (C) 1976-1995 The Santa Cruz Operation, Inc.")
        _print("="*60)
        _print(f"\nSystem time: {now().strftime('%b %d %H:%M:%S %Y')}")
        _print("Last successful connection: Dec 08 23:15:42 1995")
        _print("\n" + "-"*60)

    def login(self):
        """Performs the login process"""
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts and not self.logged_in:
            print("\n")
            username = input("login: ")
            password = getpass.getpass("Password: ")

            # Simulate processing time
            sys.stdout.write("Authenticating")
            for _ in range(3):
                time.sleep(0.3)
                sys.stdout.write(".")
                sys.stdout.flush()
            print()
            time.sleep(0.5)

            if username in self.users and self.users[username] == password:
                self.logged_in = True
                self.username = username
                self.slow_print(f"\n*** Login successful for {username} ***", 0.03)
                time.sleep(0.5)
                return True
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    self.slow_print(f"\nLogin incorrect", 0.03)
                    self.slow_print(f"Remaining attempts: {remaining}", 0.03)
                    time.sleep(0.5)

        if not self.logged_in:
            self.slow_print("\n*** Too many login failures ***", 0.03)
            self.slow_print("Disconnecting...", 0.03)
            time.sleep(1)
            self.disconnect()
            return False

    def show_welcome_message(self, username=None, print_func=None):
        """Displays welcome message after login"""
        _print = print_func if print_func else self.print_instant

        _print("\n" + "="*60)
        _print("  SCO UNIX System V/386 Release 3.2")
        _print("="*60)
        _print(f"\nLast login: {now().strftime('%a %b %d %H:%M:%S')} on tty1a")
        _print(f"Terminal: vt100")
        _print(f"\nYou have mail.")
        _print("\n" + "-"*60)
        _print("SCO UNIX System V/386 Release 3.2 (scohost)")
        _print("-"*60 + "\n")

    def logout(self, print_func=None):
        """Logout process"""
        _print = print_func if print_func else self.print_instant
        _slow_print = self.slow_print

        _print("\n" + "="*60)
        _slow_print("Closing session...", 0.03)
        time.sleep(0.5)
        _slow_print(f"Goodbye, {self.username}!", 0.03)
        _slow_print(f"Connect time: {random.randint(5, 45)} minutes", 0.03)
        time.sleep(0.5)
        self.disconnect(print_func=print_func)

    def disconnect(self, print_func=None):
        """Disconnects the modem connection"""
        _print = print_func if print_func else self.print_instant
        _slow_print = self.slow_print

        _slow_print("\nDisconnecting...", 0.03)
        time.sleep(0.5)
        _slow_print("+++ATH0", 0.03)
        time.sleep(0.3)
        _slow_print("NO CARRIER", 0.03)
        time.sleep(0.3)
        _print("\n" + "="*60)
        _print("  Connection closed")
        _print("="*60 + "\n")
        self.connected = False
        self.logged_in = False
