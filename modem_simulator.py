#!/usr/bin/env python3
"""
SCO UNIX System V/386 Modem Login Simulator
Simulates a classic modem login to a SCO UNIX System from the 1990s era
"""

import time
from vfs import VirtualFileSystem
from modem import ModemSimulator
from shell import Shell


def main():
    """Main entry point"""
    print("\nStarting SCO UNIX Modem Simulator...")
    print("(Press Ctrl+C to abort)\n")
    time.sleep(1)

    # Create virtual filesystem
    vfs = VirtualFileSystem()

    # Create modem simulator
    modem = ModemSimulator()

    try:
        # Simulate modem dial-in
        modem.simulate_modem_dial()

        # Display login screen
        modem.show_login_screen()

        # Perform login
        if modem.login():
            # Show welcome message
            modem.show_welcome_message()

            # Create and start shell with the authenticated user
            shell = Shell(modem.username, vfs)
            shell.run()

            # Logout
            modem.logout()

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        if modem.connected:
            modem.disconnect()
    except Exception as e:
        print(f"\nError: {e}")
        if modem.connected:
            modem.disconnect()

    print("\nThank you for using the SCO UNIX Simulator!")
    print("Demo credentials: root/root, sysadmin/admin123, user/password, guest/guest\n")


if __name__ == "__main__":
    main()
