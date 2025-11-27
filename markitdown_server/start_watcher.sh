#!/bin/bash

# MarkItDown Watcher Service Launcher
# This script starts the file watcher service that monitors
# /Users/syedraza/Documents/markitdown for new documents

cd "$(dirname "$0")"

echo "Starting MarkItDown File Watcher Service..."
echo ""

# Activate virtual environment and run the service
source ../.venv/bin/activate
python watcher_service.py
