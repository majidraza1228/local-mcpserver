#!/bin/bash

# Start MarkItDown MCP HTTP Server

# Activate virtual environment
source "$(dirname "$0")/../.venv/bin/activate"

# Start the MCP HTTP server
python "$(dirname "$0")/mcp_http_server.py"
