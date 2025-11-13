#!/usr/bin/env python3
"""
Modem Login Simulator
Simuliert einen klassischen Modem-Login aus der Vergangenheit
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
            "admin": "admin123",
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
        self.print_instant("     ██████╗ ██████╗ ███████╗    ██████╗ ██████╗ ███████╗")
        self.print_instant("     ██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██╔════╝")
        self.print_instant("     ██████╔╝██████╔╝███████╗    ██████╔╝██████╔╝███████╗")
        self.print_instant("     ██╔══██╗██╔══██╗╚════██║    ██╔══██╗██╔══██╗╚════██║")
        self.print_instant("     ██████╔╝██████╔╝███████║    ██████╔╝██████╔╝███████║")
        self.print_instant("     ╚═════╝ ╚═════╝ ╚══════╝    ╚═════╝ ╚═════╝ ╚══════╝")
        self.print_instant("")
        self.print_instant("     Bulletin Board System - Willkommen!")
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
        self.print_instant("  WILLKOMMEN IM SYSTEM")
        self.print_instant("="*60)
        self.print_instant(f"\nEingeloggt als: {self.username}")
        self.print_instant(f"Login-Zeit: {datetime.now().strftime('%H:%M:%S')}")
        self.print_instant(f"Terminal: VT100 Emulation")
        self.print_instant(f"\nSie haben 3 neue Nachrichten.")
        self.print_instant("Letzte Aktivität: Heute, 09:15 Uhr")
        self.print_instant("\n" + "-"*60)
        self.print_instant("Verfügbare Befehle: help, mail, files, news, who, logout")
        self.print_instant("-"*60 + "\n")

    def execute_command(self, command):
        """Führt Benutzer-Befehle aus"""
        cmd = command.strip().lower()

        if cmd == "help" or cmd == "?":
            self.print_instant("\nVerfügbare Befehle:")
            self.print_instant("-" * 40)
            self.print_instant("  help, ?     - Zeigt diese Hilfe")
            self.print_instant("  mail        - Zeigt E-Mail Posteingang")
            self.print_instant("  files       - Zeigt verfügbare Dateien")
            self.print_instant("  news        - Zeigt aktuelle Nachrichten")
            self.print_instant("  who         - Zeigt aktive Benutzer")
            self.print_instant("  time        - Zeigt aktuelle Zeit")
            self.print_instant("  about       - Über dieses System")
            self.print_instant("  logout      - Beendet die Sitzung")
            self.print_instant("-" * 40)

        elif cmd == "mail":
            self.print_instant("\n+++ E-MAIL POSTEINGANG +++")
            self.print_instant("-" * 50)
            self.print_instant("  [1] Von: sysadmin@bbs.local")
            self.print_instant("      Betreff: Systemwartung am Wochenende")
            self.print_instant("      Datum: 12.11.2025 18:34")
            self.print_instant("")
            self.print_instant("  [2] Von: newsletter@bbs.local")
            self.print_instant("      Betreff: Neue Software verfügbar")
            self.print_instant("      Datum: 11.11.2025 14:22")
            self.print_instant("")
            self.print_instant("  [3] Von: user2@bbs.local")
            self.print_instant("      Betreff: Re: Treffen nächste Woche?")
            self.print_instant("      Datum: 10.11.2025 09:15")
            self.print_instant("-" * 50)

        elif cmd == "files":
            self.print_instant("\n+++ DATEI VERZEICHNIS +++")
            self.print_instant("-" * 50)
            self.print_instant("  [DIR]  GAMES/          Spiele und Unterhaltung")
            self.print_instant("  [DIR]  UTILS/          Nützliche Programme")
            self.print_instant("  [DIR]  DOCS/           Dokumentation")
            self.print_instant("  [FILE] README.TXT      Willkommens-Datei (2 KB)")
            self.print_instant("  [FILE] NEWS.TXT        Neuigkeiten (5 KB)")
            self.print_instant("  [FILE] USERS.LST       Benutzerliste (1 KB)")
            self.print_instant("-" * 50)
            self.print_instant("Gesamt: 3 Verzeichnisse, 3 Dateien")

        elif cmd == "news":
            self.print_instant("\n+++ AKTUELLE NACHRICHTEN +++")
            self.print_instant("-" * 50)
            self.print_instant("13.11.2025 - Neue 28.8k Modems verfügbar!")
            self.print_instant("12.11.2025 - Systemupgrade erfolgreich")
            self.print_instant("10.11.2025 - Neue Dateien im GAMES Bereich")
            self.print_instant("08.11.2025 - Wartungsarbeiten abgeschlossen")
            self.print_instant("-" * 50)

        elif cmd == "who":
            self.print_instant("\n+++ AKTIVE BENUTZER +++")
            self.print_instant("-" * 50)
            self.print_instant(f"  {self.username:<12} Terminal 1   Login: {datetime.now().strftime('%H:%M')}")
            self.print_instant(f"  user2        Terminal 3   Login: 14:22")
            self.print_instant(f"  guest001     Terminal 5   Login: 15:01")
            self.print_instant("-" * 50)
            self.print_instant("Gesamt: 3 Benutzer online")

        elif cmd == "time":
            self.print_instant(f"\nAktuelle Systemzeit: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")

        elif cmd == "about":
            self.print_instant("\n+++ ÜBER DIESES SYSTEM +++")
            self.print_instant("-" * 50)
            self.print_instant("BBS System v2.4")
            self.print_instant("Betriebssystem: UNIX System V")
            self.print_instant("Modem: US Robotics Sportster 14.4k")
            self.print_instant("Online seit: Januar 1995")
            self.print_instant("\nEin Retro-Modem-Simulator von 2025")
            self.print_instant("Simuliert die Erfahrung der frühen Internet-Ära")
            self.print_instant("-" * 50)

        elif cmd == "logout" or cmd == "exit" or cmd == "quit":
            return False

        elif cmd == "":
            pass  # Leere Eingabe ignorieren

        else:
            self.print_instant(f"\nUnbekannter Befehl: '{command}'")
            self.print_instant("Geben Sie 'help' für eine Liste der Befehle ein.")

        return True

    def interactive_shell(self):
        """Interaktive Shell nach erfolgreichem Login"""
        self.show_welcome_message()

        while True:
            try:
                command = input(f"\n{self.username}@BBS> ")

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
    print("\nStarte Modem-Simulator...")
    print("(Drücken Sie Ctrl+C zum Abbrechen)\n")
    time.sleep(1)

    simulator = ModemSimulator()
    simulator.run()

    print("\nVielen Dank für die Nutzung des Modem-Simulators!")
    print("Demo-Zugangsdaten: admin/admin123, user/password, guest/guest\n")

if __name__ == "__main__":
    main()
