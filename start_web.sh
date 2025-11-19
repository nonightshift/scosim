#!/bin/bash
#
# Start script for SCO Unix Simulator Web Server
# Provides browser-based access to the modem simulator
#

echo "=================================================="
echo "  SCO Unix System V/386 - Web Terminal Server"
echo "=================================================="
echo ""
echo "Starting web server..."
echo ""
echo "Access the terminal in your browser at:"
echo "  http://localhost:5000"
echo ""
echo "Or from other devices on your network at:"
echo "  http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "=================================================="
echo ""

# Check if dependencies are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "ERROR: Flask is not installed!"
    echo "Please install dependencies first:"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 1
fi

if ! python3 -c "import flask_socketio" 2>/dev/null; then
    echo "ERROR: Flask-SocketIO is not installed!"
    echo "Please install dependencies first:"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 1
fi

# Start the web server
python3 web_server.py
