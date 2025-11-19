# SCO UNIX System V/386 Modem Login Simulator

Ein Python-basierter Kommandozeilensimulator, der die authentische Erfahrung eines Modem-Logins zu einem SCO UNIX System V/386 aus den 1990er Jahren nachbildet. Perfekt für Nostalgie, Bildungszwecke oder einfach zum Spaß!

## Features

- **Authentische Modem-Einwahl**: Simuliert den kompletten Einwahlprozess mit AT-Befehlen und Modem-Geräuschen
- **SCO UNIX System**: Klassischer Login-Bildschirm mit ASCII-Art für SCO UNIX System V/386
- **UNIX Shell**: Echte UNIX-Kommandos mit authentischen Ausgaben
- **Realistische Verzögerungen**: Simuliert die langsame Verbindungsgeschwindigkeit der damaligen Zeit
- **Passwort-Authentifizierung**: Sicheres Login-System mit mehreren Demo-Benutzern
- **Root-Zugang**: Simuliert einen root-Login mit # Prompt

## Was wird simuliert?

Der Simulator bildet folgende Elemente nach:

1. **Modem-Initialisierung**: AT-Befehle (ATZ, ATE1, ATM1, etc.)
2. **Wählvorgang**: Akustische Wählsignale (als Text dargestellt)
3. **Handshake**: Die charakteristischen Modem-Geräusche beim Verbindungsaufbau
4. **Verbindungsaufbau**: "CONNECT 14400/V.32bis" Nachricht
5. **SCO UNIX System**: SCO UNIX System V/386 mit ASCII-Art Logo
6. **Login-Prozess**: Benutzername/Passwort Eingabe mit Authentifizierung
7. **UNIX Shell**: Echte UNIX-Kommandos wie ls, ps, df, who, uname, etc.
8. **Root-Prompt**: Authentischer # Prompt für root-Benutzer
9. **Verbindungsabbau**: Ordentliches Logout mit "NO CARRIER" Nachricht

## Installation

### Voraussetzungen

- Python 3.6 oder höher
- Keine externen Bibliotheken erforderlich (verwendet nur Python Standard-Bibliothek)

### Setup

1. Repository klonen oder Dateien herunterladen:
```bash
git clone <repository-url>
cd scosim
```

2. Skript ausführbar machen (optional, Unix/Linux):
```bash
chmod +x modem_simulator.py
```

## Verwendung

### Option 1: Terminal-Version

Starten Sie den Simulator im Terminal mit:

```bash
python3 modem_simulator.py
```

oder (wenn ausführbar gemacht):

```bash
./modem_simulator.py
```

oder mit dem Startskript:

```bash
./start.sh
```

### Option 2: Web-Terminal (Browser-Zugriff)

**NEU!** Der Simulator kann jetzt über einen Webbrowser mit einem minimalen Custom-Terminal verwendet werden:

#### Installation der Web-Abhängigkeiten

```bash
pip install -r requirements.txt
```

Dies installiert:
- Flask (Web-Framework)
- Flask-SocketIO (WebSocket-Unterstützung)
- python-socketio (Socket.IO Backend)
- eventlet (Async-Server)

#### Starten des Web-Servers

```bash
./start_web.sh
```

oder direkt:

```bash
python3 web_server.py
```

#### Zugriff auf das Web-Terminal

Öffnen Sie Ihren Browser und navigieren Sie zu:

- **Lokal**: http://localhost:5000
- **Im Netzwerk**: http://[IP-Adresse]:5000

Das Web-Terminal bietet:
- ✅ Minimales Custom-Terminal ohne externe Dependencies
- ✅ Authentisches grünes Retro-Terminal-Design
- ✅ ANSI-Farb-Unterstützung für farbige Ausgaben
- ✅ WebSocket-Verbindung für schnelle Kommunikation
- ✅ Alle UNIX-Befehle wie in der Terminal-Version
- ✅ Zugriff von überall im Netzwerk
- ✅ Keine Installation auf Client-Seite erforderlich
- ✅ Mehrere simultane Benutzer-Sitzungen möglich
- ✅ Responsive Design für Desktop und Mobile

### Demo-Zugangsdaten

Das System enthält vier vorkonfigurierte Benutzer-Accounts:

| Benutzername | Passwort   | Beschreibung        |
|--------------|-----------|---------------------|
| root         | root      | Root-Benutzer (#)   |
| sysadmin     | admin123  | Systemadministrator |
| user         | password  | Normaler Benutzer   |
| guest        | guest     | Gast-Benutzer       |

### Verfügbare UNIX-Befehle

Nach erfolgreichem Login stehen folgende UNIX-Befehle zur Verfügung:

- `ls [-l]` - Verzeichnisinhalt anzeigen
- `pwd` - Aktuelles Verzeichnis anzeigen
- `date` - Datum und Uhrzeit anzeigen
- `who` - Eingeloggte Benutzer anzeigen
- `w` - Benutzer und ihre Aktivitäten
- `whoami` - Aktuellen Benutzernamen anzeigen
- `uptime` - System-Laufzeit anzeigen
- `df` - Dateisystem-Belegung anzeigen
- `ps [-ef]` - Prozesse anzeigen
- `uname [-a]` - System-Informationen anzeigen
- `cat <file>` - Dateiinhalt anzeigen (z.B. /etc/motd, .profile)
- `clear` - Bildschirm löschen
- `help` - Zeigt diese Hilfe
- `exit` / `logout` - Beendet die Sitzung und trennt die Verbindung

## Beispiel-Sitzung

```
Starte SCO UNIX Modem-Simulator...
(Drücken Sie Ctrl+C zum Abbrechen)

============================================================
     MODEM KOMMUNIKATIONS SIMULATOR v2.4
     Copyright (C) 1995-1998
============================================================

Initialisiere Modem...
AT
OK
ATZ
OK
ATE1
OK
ATM1
OK
ATX4
OK
ATDT 555-1234

Wähle Nummer...
BEEP BEEP BEEP BEEP BEEP BEEP BEEP

Verbinde...
RRRRR.....
KSSSSSHHHHhhhh....
BEEEEeeeeee....
WRRRRrrrrrr....
CHHHhhhhh....

CONNECT 14400/V.32bis

============================================================

     ███████╗ ██████╗ ██████╗     ██╗   ██╗███╗   ██╗██╗██╗  ██╗
     ██╔════╝██╔════╝██╔═══██╗    ██║   ██║████╗  ██║██║╚██╗██╔╝
     ███████╗██║     ██║   ██║    ██║   ██║██╔██╗ ██║██║ ╚███╔╝
     ╚════██║██║     ██║   ██║    ██║   ██║██║╚██╗██║██║ ██╔██╗
     ███████║╚██████╗╚██████╔╝    ╚██████╔╝██║ ╚████║██║██╔╝ ██╗
     ╚══════╝ ╚═════╝ ╚═════╝      ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝

     SCO UNIX System V/386 Release 3.2
     Copyright (C) 1976-1995 The Santa Cruz Operation, Inc.
============================================================

Benutzername: root
Passwort:
Authentifiziere...

*** Login erfolgreich! Willkommen root! ***

============================================================
  SCO UNIX System V/386 Release 3.2
============================================================

Last login: Wed Nov 13 15:42:18 on tty1a
Terminal: vt100

You have mail.

------------------------------------------------------------
SCO UNIX System V/386 Release 3.2 (scohost)
------------------------------------------------------------

# uname -a
SCO_SV scohost 3.2 2 i386
# whoami
root
# ls -l
total 48
drwxr-xr-x   2 root     sys         512 Nov 12 14:32 bin
drwxr-xr-x   4 root     sys        1024 Nov 13 09:15 etc
drwxr-xr-x   3 root     sys         512 Nov 10 16:45 home
drwxr-xr-x   8 root     sys        2048 Nov 11 11:20 usr
drwxr-xr-x   2 root     sys         512 Nov 13 10:05 tmp
drwxr-xr-x   3 root     sys        1024 Nov 12 18:30 var
-rw-r--r--   1 root     sys        1847 Nov 10 14:22 .profile
-rw-------   1 root     sys         256 Nov 13 08:45 .history
# uptime
 15:42:35  up 23 days,  4:32,  3 users,  load average: 0.15, 0.21, 0.18
# logout
```

## Technische Details

### Architektur

Der Simulator ist als Python-Klasse `ModemSimulator` implementiert mit folgenden Hauptkomponenten:

- **simulate_modem_dial()**: Simuliert den kompletten Modem-Einwahlprozess
- **show_login_screen()**: Zeigt den SCO UNIX Login-Bildschirm
- **login()**: Verarbeitet die Benutzer-Authentifizierung
- **interactive_shell()**: Hauptschleife für die UNIX Shell mit root/user Prompt
- **execute_command()**: Verarbeitet UNIX-Befehle (ls, ps, who, etc.)
- **disconnect()**: Trennt die Modem-Verbindung

### Spezielle Effekte

- **slow_print()**: Gibt Text Zeichen für Zeichen aus für den authentischen Retro-Look
- **Zeitverzögerungen**: Simuliert die langsame Geschwindigkeit von 14.4k Modems
- **AT-Befehle**: Echte Hayes-AT-Befehlssequenzen aus der Modem-Ära

## Anpassung

### Eigene Benutzer hinzufügen

Bearbeiten Sie das `self.users` Dictionary in der `__init__` Methode:

```python
self.users = {
    "meinname": "meinpasswort",
    "anderer": "passwort123"
}
```

**Hinweis**: In einer produktiven Umgebung sollten Passwörter niemals im Klartext gespeichert werden!

### Neue Befehle hinzufügen

Fügen Sie neue Befehle in der `execute_command()` Methode hinzu:

```python
elif cmd == "meinbefehl":
    self.print_instant("\nDas ist mein eigener Befehl!")
    # Ihre Logik hier
```

### Geschwindigkeit anpassen

Die Geschwindigkeit der Textausgabe kann durch Änderung der `delay` Parameter angepasst werden:

```python
self.slow_print("Text", delay=0.05)  # Standard
self.slow_print("Schneller", delay=0.01)
self.slow_print("Langsamer", delay=0.1)
```

## Hintergrund

Dieser Simulator wurde erstellt, um die Erfahrung der frühen Internet-Ära zu bewahren, als Menschen sich per Modem über Telefonleitungen zu UNIX-Systemen einwählten. In den 1990er Jahren waren:

- **SCO UNIX**: SCO (Santa Cruz Operation) UNIX System V/386 war eines der populärsten kommerziellen UNIX-Systeme für Intel x86 Prozessoren
- **Modem-Geschwindigkeiten**: 14.4k, 28.8k, später 56k
- **Terminal-Zugang**: Einwahl per Modem zu UNIX-Systemen war eine gängige Remote-Access-Methode
- **AT-Befehle**: Hayes-kompatible AT-Befehle zur Modem-Steuerung
- **Verbindungsgeräusche**: Die charakteristischen Piep- und Rauschgeräusche beim Verbindungsaufbau
- **VT100-Terminals**: VT100-kompatible Terminal-Emulation war der Standard

## Lizenz

Dieses Projekt ist für Bildungs- und Unterhaltungszwecke gedacht. Frei verwendbar und anpassbar.

## Autor

Erstellt mit Claude AI im November 2025.

## Problembehandlung

### Das Programm reagiert nicht

- Drücken Sie `Ctrl+C` um das Programm zu beenden
- Überprüfen Sie, ob Python 3 korrekt installiert ist: `python3 --version`

### Passwort-Eingabe wird angezeigt

Das Programm verwendet `getpass.getpass()` um Passwörter sicher einzugeben. In einigen Terminals wird das Passwort nicht angezeigt (wie gewünscht).

### Umlaute werden nicht korrekt angezeigt

Stellen Sie sicher, dass Ihr Terminal UTF-8 Encoding unterstützt:
```bash
export LANG=de_DE.UTF-8
```

## Verbesserungsideen

Mögliche Erweiterungen für die Zukunft:

- [x] **Web-Terminal mit Custom HTML/CSS/JS** (✅ Implementiert!)
- [x] **Multi-User Support mit Netzwerk-Kommunikation** (✅ Implementiert via Web-Server!)
- [ ] Mehr UNIX-Befehle (vi, grep, find, etc.)
- [ ] Dateisystem-Simulation mit echten Verzeichnisoperationen
- [ ] Konfigurationsdatei für Benutzer und Einstellungen
- [ ] Verschiedene Modem-Geschwindigkeiten wählbar
- [ ] Sound-Effekte (echte Modem-Geräusche)
- [ ] Mail-System Simulation (mailx)
- [ ] UNIX-Prozess-Simulation mit echten Interaktionen

## Feedback

Haben Sie Ideen für Verbesserungen oder haben Sie einen Fehler gefunden? Erstellen Sie gerne ein Issue oder Pull Request!
