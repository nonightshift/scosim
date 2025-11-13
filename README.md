# Modem Login Simulator

Ein Python-basierter Kommandozeilensimulator, der die authentische Erfahrung eines Modem-Logins aus den 1990er Jahren nachbildet. Perfekt für Nostalgie, Bildungszwecke oder einfach zum Spaß!

## Features

- **Authentische Modem-Einwahl**: Simuliert den kompletten Einwahlprozess mit AT-Befehlen und Modem-Geräuschen
- **Retro BBS-Login**: Klassischer Login-Bildschirm mit ASCII-Art
- **Interaktive Shell**: Verschiedene Befehle zum Erkunden des Systems
- **Realistische Verzögerungen**: Simuliert die langsame Verbindungsgeschwindigkeit der damaligen Zeit
- **Passwort-Authentifizierung**: Sicheres Login-System mit mehreren Demo-Benutzern

## Was wird simuliert?

Der Simulator bildet folgende Elemente nach:

1. **Modem-Initialisierung**: AT-Befehle (ATZ, ATE1, ATM1, etc.)
2. **Wählvorgang**: Akustische Wählsignale (als Text dargestellt)
3. **Handshake**: Die charakteristischen Modem-Geräusche beim Verbindungsaufbau
4. **Verbindungsaufbau**: "CONNECT 14400/V.32bis" Nachricht
5. **BBS-System**: Bulletin Board System mit ASCII-Art Logo
6. **Login-Prozess**: Benutzername/Passwort Eingabe mit Authentifizierung
7. **Interaktive Shell**: Verschiedene Befehle wie Mail, Files, News, etc.
8. **Verbindungsabbau**: Ordentliches Logout mit "NO CARRIER" Nachricht

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

Starten Sie den Simulator einfach mit:

```bash
python3 modem_simulator.py
```

oder (wenn ausführbar gemacht):

```bash
./modem_simulator.py
```

### Demo-Zugangsdaten

Das System enthält drei vorkonfigurierte Benutzer-Accounts:

| Benutzername | Passwort   |
|--------------|-----------|
| admin        | admin123  |
| user         | password  |
| guest        | guest     |

### Verfügbare Befehle

Nach erfolgreichem Login stehen folgende Befehle zur Verfügung:

- `help` oder `?` - Zeigt die Hilfe mit allen verfügbaren Befehlen
- `mail` - Zeigt den E-Mail Posteingang mit Beispiel-Nachrichten
- `files` - Zeigt ein Dateiverzeichnis mit Ordnern und Dateien
- `news` - Zeigt aktuelle System-Nachrichten
- `who` - Zeigt eine Liste der aktuell eingeloggten Benutzer
- `time` - Zeigt die aktuelle Systemzeit
- `about` - Informationen über das System
- `logout` - Beendet die Sitzung und trennt die Verbindung

## Beispiel-Sitzung

```
Starte Modem-Simulator...
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

     ██████╗ ██████╗ ███████╗    ██████╗ ██████╗ ███████╗
     ██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██╔════╝
     ██████╔╝██████╔╝███████╗    ██████╔╝██████╔╝███████╗
     ██╔══██╗██╔══██╗╚════██║    ██╔══██╗██╔══██╗╚════██║
     ██████╔╝██████╔╝███████║    ██████╔╝██████╔╝███████║
     ╚═════╝ ╚═════╝ ╚══════╝    ╚═════╝ ╚═════╝ ╚══════╝

     Bulletin Board System - Willkommen!
============================================================

Benutzername: admin
Passwort:
Authentifiziere...

*** Login erfolgreich! Willkommen admin! ***

admin@BBS> help
admin@BBS> mail
admin@BBS> logout
```

## Technische Details

### Architektur

Der Simulator ist als Python-Klasse `ModemSimulator` implementiert mit folgenden Hauptkomponenten:

- **simulate_modem_dial()**: Simuliert den kompletten Modem-Einwahlprozess
- **show_login_screen()**: Zeigt den BBS-Login-Bildschirm
- **login()**: Verarbeitet die Benutzer-Authentifizierung
- **interactive_shell()**: Hauptschleife für die Benutzerinteraktion
- **execute_command()**: Verarbeitet eingegebene Befehle
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

Dieser Simulator wurde erstellt, um die Erfahrung der frühen Internet-Ära zu bewahren, als Menschen sich per Modem über Telefonleitungen ins Internet einwählten. In den 1990er Jahren waren:

- **Modem-Geschwindigkeiten**: 14.4k, 28.8k, später 56k
- **BBS-Systeme**: Bulletin Board Systems waren vor dem World Wide Web populär
- **AT-Befehle**: Hayes-kompatible AT-Befehle zur Modem-Steuerung
- **Verbindungsgeräusche**: Die charakteristischen Piep- und Rauschgeräusche beim Verbindungsaufbau

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

- [ ] Mehr interaktive Befehle (Chat, Games, Downloads)
- [ ] Konfigurationsdatei für Benutzer und Einstellungen
- [ ] Verschiedene Modem-Geschwindigkeiten wählbar
- [ ] Sound-Effekte (echte Modem-Geräusche)
- [ ] Multi-User Support mit echter Netzwerk-Kommunikation
- [ ] Datei-Upload/Download Simulation
- [ ] ASCII-Art Spiele und Programme

## Feedback

Haben Sie Ideen für Verbesserungen oder haben Sie einen Fehler gefunden? Erstellen Sie gerne ein Issue oder Pull Request!
