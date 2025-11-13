#!/usr/bin/env python3
"""
SCO UNIX System V/386 Modem Login Simulator
Simuliert einen klassischen Modem-Login zu einem SCO UNIX System aus den 1990er Jahren
"""

import sys
import time
import random
import getpass
from datetime import datetime

class ModemSimulator:
    def __init__(self):
        self.connected = False
        self.logged_in = False
        self.username = None

        # Standardbenutzer für Demo (in der Praxis sollten Passwörter gehasht werden)
        self.users = {
            "root": "root",
            "sysadmin": "admin123",
            "user": "password",
            "guest": "guest"
        }

    def slow_print(self, text, delay=0.05):
        """Gibt Text Zeichen für Zeichen aus für authentischen Retro-Effekt"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def print_instant(self, text):
        """Gibt Text sofort aus"""
        print(text)

    def simulate_modem_dial(self):
        """Simuliert den Modem-Einwahlprozess"""
        self.print_instant("\n" + "="*60)
        self.print_instant("     MODEM KOMMUNIKATIONS SIMULATOR v2.4")
        self.print_instant("     Copyright (C) 1995-1998")
        self.print_instant("="*60 + "\n")

        time.sleep(0.5)
        self.slow_print("Initialisiere Modem...", 0.03)
        time.sleep(0.3)

        # AT-Befehle
        at_commands = [
            ("AT", "OK"),
            ("ATZ", "OK"),
            ("ATE1", "OK"),
            ("ATM1", "OK"),
            ("ATX4", "OK"),
            ("ATDT 555-1234", "")
        ]

        for cmd, response in at_commands:
            self.slow_print(f"{cmd}", 0.02)
            time.sleep(0.2)
            if response:
                self.slow_print(response, 0.02)
            time.sleep(0.3)

        # Wählgeräusche simulieren
        self.print_instant("")
        self.slow_print("Wähle Nummer...", 0.04)
        time.sleep(0.5)

        dial_sounds = ["BEEP", "BEEP", "BEEP", "BEEP", "BEEP", "BEEP", "BEEP"]
        for sound in dial_sounds:
            sys.stdout.write(sound + " ")
            sys.stdout.flush()
            time.sleep(0.15)
        print("\n")

        time.sleep(0.5)
        self.slow_print("Verbinde...", 0.04)
        time.sleep(0.8)

        # Modem-Handshake Geräusche als Text
        handshake = [
            "RRRRR.....",
            "KSSSSSHHHHhhhh....",
            "BEEEEeeeeee....",
            "WRRRRrrrrrr....",
            "CHHHhhhhh...."
        ]

        for sound in handshake:
            self.slow_print(sound, 0.02)
            time.sleep(0.3)

        time.sleep(0.5)
        self.print_instant("")
        self.slow_print("CONNECT 14400/V.32bis", 0.03)
        self.connected = True
        time.sleep(0.5)

    def show_login_screen(self):
        """Zeigt den Login-Bildschirm"""
        self.print_instant("\n" + "="*60)
        self.print_instant("")
        self.print_instant("     ███████╗ ██████╗ ██████╗     ██╗   ██╗███╗   ██╗██╗██╗  ██╗")
        self.print_instant("     ██╔════╝██╔════╝██╔═══██╗    ██║   ██║████╗  ██║██║╚██╗██╔╝")
        self.print_instant("     ███████╗██║     ██║   ██║    ██║   ██║██╔██╗ ██║██║ ╚███╔╝ ")
        self.print_instant("     ╚════██║██║     ██║   ██║    ██║   ██║██║╚██╗██║██║ ██╔██╗ ")
        self.print_instant("     ███████║╚██████╗╚██████╔╝    ╚██████╔╝██║ ╚████║██║██╔╝ ██╗")
        self.print_instant("     ╚══════╝ ╚═════╝ ╚═════╝      ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝")
        self.print_instant("")
        self.print_instant("     SCO UNIX System V/386 Release 3.2")
        self.print_instant("     Copyright (C) 1976-1995 The Santa Cruz Operation, Inc.")
        self.print_instant("="*60)
        self.print_instant(f"\nSystem Zeit: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        self.print_instant("Letzte erfolgreiche Verbindung: 13.11.2025 14:32:18")
        self.print_instant("\n" + "-"*60)

    def login(self):
        """Führt den Login-Prozess durch"""
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts and not self.logged_in:
            print("\n")
            username = input("Benutzername: ")
            password = getpass.getpass("Passwort: ")

            # Simuliere Verarbeitungszeit
            sys.stdout.write("Authentifiziere")
            for _ in range(3):
                time.sleep(0.3)
                sys.stdout.write(".")
                sys.stdout.flush()
            print()
            time.sleep(0.5)

            if username in self.users and self.users[username] == password:
                self.logged_in = True
                self.username = username
                self.slow_print(f"\n*** Login erfolgreich! Willkommen {username}! ***", 0.03)
                time.sleep(0.5)
                return True
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    self.slow_print(f"\n*** FEHLER: Ungültige Anmeldedaten ***", 0.03)
                    self.slow_print(f"Verbleibende Versuche: {remaining}", 0.03)
                    time.sleep(0.5)

        if not self.logged_in:
            self.slow_print("\n*** Maximale Anzahl von Versuchen erreicht ***", 0.03)
            self.slow_print("Verbindung wird getrennt...", 0.03)
            time.sleep(1)
            self.disconnect()
            return False

    def show_welcome_message(self):
        """Zeigt Willkommensnachricht nach Login"""
        self.print_instant("\n" + "="*60)
        self.print_instant("  SCO UNIX System V/386 Release 3.2")
        self.print_instant("="*60)
        self.print_instant(f"\nLast login: {datetime.now().strftime('%a %b %d %H:%M:%S')} on tty1a")
        self.print_instant(f"Terminal: vt100")
        self.print_instant(f"\nYou have mail.")
        self.print_instant("\n" + "-"*60)
        self.print_instant("SCO UNIX System V/386 Release 3.2 (scohost)")
        self.print_instant("-"*60 + "\n")

    def execute_command(self, command):
        """Führt Unix-Befehle aus"""
        parts = command.strip().split()
        if not parts:
            return True

        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        if cmd == "ls":
            if "-l" in args:
                self.print_instant("total 48")
                self.print_instant("drwxr-xr-x   2 root     sys         512 Nov 12 14:32 bin")
                self.print_instant("drwxr-xr-x   4 root     sys        1024 Nov 13 09:15 etc")
                self.print_instant("drwxr-xr-x   3 root     sys         512 Nov 10 16:45 home")
                self.print_instant("drwxr-xr-x   8 root     sys        2048 Nov 11 11:20 usr")
                self.print_instant("drwxr-xr-x   2 root     sys         512 Nov 13 10:05 tmp")
                self.print_instant("drwxr-xr-x   3 root     sys        1024 Nov 12 18:30 var")
                self.print_instant("-rw-r--r--   1 root     sys        1847 Nov 10 14:22 .profile")
                self.print_instant("-rw-------   1 root     sys         256 Nov 13 08:45 .history")
            else:
                self.print_instant("bin\tetc\thome\tusr\ttmp\tvar\t.profile")

        elif cmd == "pwd":
            self.print_instant("/")

        elif cmd == "date":
            self.print_instant(datetime.now().strftime('%a %b %d %H:%M:%S %Z %Y'))

        elif cmd == "who":
            self.print_instant(f"{self.username:<12} tty1a        {datetime.now().strftime('%b %d %H:%M')}")
            self.print_instant(f"operator     tty2         {datetime.now().strftime('%b %d')} 09:15")
            self.print_instant(f"admin        tty3         {datetime.now().strftime('%b %d')} 14:22")

        elif cmd == "w" or cmd == "whoami":
            if cmd == "whoami":
                self.print_instant(self.username)
            else:
                current_time = datetime.now().strftime('%H:%M:%S')
                self.print_instant(f" {current_time}  up 23 days,  4:32,  3 users")
                self.print_instant(f"User     tty       login@  idle   what")
                self.print_instant(f"{self.username:<8} tty1a     {datetime.now().strftime('%H:%M')}    0     -sh")
                self.print_instant(f"operator tty2      09:15    1:45  /usr/bin/vi")
                self.print_instant(f"admin    tty3      14:22    0:12  /bin/sh")

        elif cmd == "uptime":
            self.print_instant(f" {datetime.now().strftime('%H:%M:%S')}  up 23 days,  4:32,  3 users,  load average: 0.15, 0.21, 0.18")

        elif cmd == "df":
            self.print_instant("Filesystem            kbytes    used   avail capacity  Mounted on")
            self.print_instant("/dev/root              51200   28672   22528    56%    /")
            self.print_instant("/dev/u                256000  189440   66560    74%    /u")
            self.print_instant("/dev/swap              65536   12288   53248    19%    swap")

        elif cmd == "ps":
            if "-ef" in args or "-aux" in args:
                self.print_instant("  UID   PID  PPID  C    STIME TTY      TIME COMMAND")
                self.print_instant("  root     1     0  0 Nov 01  ?        0:03 /etc/init")
                self.print_instant("  root    23     1  0 Nov 01  ?        0:00 /etc/cron")
                self.print_instant("  root    45     1  0 Nov 01  ?        0:12 /etc/syslogd")
                self.print_instant(f"  {self.username:<8}{random.randint(100,999)}     1  0 {datetime.now().strftime('%H:%M')}  tty1a    0:00 -sh")
                self.print_instant("  root   156     1  0 Nov 02  ?        1:23 /usr/lib/sendmail")
                self.print_instant("  root   234     1  0 Nov 03  ?        0:45 /usr/sbin/inetd")
            else:
                self.print_instant("  PID TTY      TIME COMMAND")
                self.print_instant(f" {random.randint(100,999)} tty1a    0:00 sh")
                self.print_instant(f" {random.randint(100,999)} tty1a    0:00 ps")

        elif cmd == "uname":
            if "-a" in args:
                self.print_instant("SCO_SV scohost 3.2 2 i386")
            else:
                self.print_instant("SCO_SV")

        elif cmd == "cat":
            if args:
                if args[0] == "/etc/motd":
                    self.print_instant("\nSCO UNIX System V/386 Release 3.2")
                    self.print_instant("Copyright (C) 1976-1995 The Santa Cruz Operation, Inc.")
                    self.print_instant("\nWelcome to SCO UNIX!")
                    self.print_instant("For technical support, contact your system administrator.")
                elif args[0] == ".profile":
                    self.print_instant("# .profile for root")
                    self.print_instant("PATH=/bin:/usr/bin:/etc:/usr/sbin")
                    self.print_instant("export PATH")
                    self.print_instant("PS1='# '")
                    self.print_instant("TERM=vt100")
                    self.print_instant("export TERM")
                else:
                    self.print_instant(f"cat: cannot open {args[0]}: No such file or directory")
            else:
                self.print_instant("Usage: cat filename")

        elif cmd == "clear":
            # Einfaches Clear durch viele Leerzeilen
            print("\n" * 50)

        elif cmd == "help":
            self.print_instant("\nVerfügbare UNIX-Befehle:")
            self.print_instant("-" * 60)
            self.print_instant("  ls [-l]         - Verzeichnisinhalt anzeigen")
            self.print_instant("  pwd             - Aktuelles Verzeichnis anzeigen")
            self.print_instant("  date            - Datum und Uhrzeit anzeigen")
            self.print_instant("  who             - Eingeloggte Benutzer anzeigen")
            self.print_instant("  w               - Benutzer und ihre Aktivitäten")
            self.print_instant("  whoami          - Aktuellen Benutzernamen anzeigen")
            self.print_instant("  uptime          - System-Laufzeit anzeigen")
            self.print_instant("  df              - Dateisystem-Belegung anzeigen")
            self.print_instant("  ps [-ef]        - Prozesse anzeigen")
            self.print_instant("  uname [-a]      - System-Informationen anzeigen")
            self.print_instant("  cat <file>      - Dateiinhalt anzeigen")
            self.print_instant("  clear           - Bildschirm löschen")
            self.print_instant("  exit, logout    - Abmelden")
            self.print_instant("-" * 60)

        elif cmd == "logout" or cmd == "exit" or cmd == "quit":
            return False

        else:
            self.print_instant(f"{cmd}: not found")

        return True

    def interactive_shell(self):
        """Interaktive Shell nach erfolgreichem Login"""
        self.show_welcome_message()

        while True:
            try:
                # Unix root prompt
                if self.username == "root":
                    prompt = "# "
                else:
                    prompt = "$ "

                command = input(prompt)

                if not self.execute_command(command):
                    break

            except KeyboardInterrupt:
                print("\n")
                confirm = input("Möchten Sie wirklich ausloggen? (j/n): ")
                if confirm.lower() in ['j', 'y', 'yes', 'ja']:
                    break
            except EOFError:
                break

        self.logout()

    def logout(self):
        """Logout-Prozess"""
        self.print_instant("\n" + "="*60)
        self.slow_print("Beende Sitzung...", 0.03)
        time.sleep(0.5)
        self.slow_print(f"Auf Wiedersehen, {self.username}!", 0.03)
        self.slow_print(f"Verbindungszeit: {random.randint(5, 45)} Minuten", 0.03)
        time.sleep(0.5)
        self.disconnect()

    def disconnect(self):
        """Trennt die Modem-Verbindung"""
        self.slow_print("\nTrenne Verbindung...", 0.03)
        time.sleep(0.5)
        self.slow_print("+++ATH0", 0.03)
        time.sleep(0.3)
        self.slow_print("NO CARRIER", 0.03)
        time.sleep(0.3)
        self.print_instant("\n" + "="*60)
        self.print_instant("  Verbindung getrennt")
        self.print_instant("="*60 + "\n")
        self.connected = False
        self.logged_in = False

    def run(self):
        """Hauptprogramm"""
        try:
            # Modem-Einwahl simulieren
            self.simulate_modem_dial()

            # Login-Bildschirm anzeigen
            self.show_login_screen()

            # Login durchführen
            if self.login():
                # Interaktive Shell starten
                self.interactive_shell()

        except KeyboardInterrupt:
            print("\n\nProgramm durch Benutzer unterbrochen.")
            if self.connected:
                self.disconnect()
        except Exception as e:
            print(f"\nFehler: {e}")
            if self.connected:
                self.disconnect()

def main():
    """Haupteinstiegspunkt"""
    print("\nStarte SCO UNIX Modem-Simulator...")
    print("(Drücken Sie Ctrl+C zum Abbrechen)\n")
    time.sleep(1)

    simulator = ModemSimulator()
    simulator.run()

    print("\nVielen Dank für die Nutzung des SCO UNIX Simulators!")
    print("Demo-Zugangsdaten: root/root, sysadmin/admin123, user/password, guest/guest\n")

if __name__ == "__main__":
    main()
