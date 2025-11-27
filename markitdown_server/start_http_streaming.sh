#!/bin/bash
cd "$(dirname "$0")/.."
exec .venv/bin/python markitdown_server/http_streaming_server.py
