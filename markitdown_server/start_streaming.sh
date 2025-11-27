#!/bin/bash

# Start MarkItDown Streaming Server

# Activate virtual environment
source "$(dirname "$0")/../.venv/bin/activate"

# Start the streaming server
python "$(dirname "$0")/streaming_server.py"
