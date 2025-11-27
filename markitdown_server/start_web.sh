#!/bin/bash

# MarkItDown Web Server Launcher
# Starts the FastAPI web interface on http://localhost:8000

cd "$(dirname "$0")"

echo "Starting MarkItDown Web Server..."
echo ""

# Activate virtual environment and run the web server
source ../.venv/bin/activate
python web_server.py
