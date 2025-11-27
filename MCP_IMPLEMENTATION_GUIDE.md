# MarkItDown MCP Implementation Guide

## Overview

This project demonstrates **three different implementations** of the MarkItDown document conversion service:

1. **MCP Server** (AI Assistant Integration) ✅ **MCP Protocol Implemented**
2. **Web Server** (Browser Interface) ❌ **Regular FastAPI, No MCP**
3. **File Watcher** (Automated Processing) ❌ **Standalone Service, No MCP**

---

## 1. MCP Server Implementation ✅

**File:** `markitdown_server/server.py`

### What Makes It MCP?

```python
from fastmcp import FastMCP  # ← Using FastMCP framework

# Initialize MCP server
app = FastMCP(
    name="markitdown",
    instructions="Convert files and URLs to Markdown format"
)

# Define MCP tools using decorators
@app.tool(description="Convert a local file to Markdown")
def convert_file(path: str):
    """MCP Tool: Accessible through MCP protocol"""
    # ... implementation

@app.tool(description="Convert a URL to Markdown")
def convert_url(url: str):
    """MCP Tool: Accessible through MCP protocol"""
    # ... implementation
```

### Key MCP Features:

✅ **Uses FastMCP Framework**
- Built on Model Context Protocol specification
- STDIO transport for communication
- Tool discovery and invocation protocol

✅ **Exposes MCP Tools:**
- `convert_file(path)` - Convert local files
- `convert_url(url)` - Convert web pages
- `convert_batch(paths)` - Batch conversion
- `get_supported_formats()` - List formats

✅ **MCP Configuration:**
```json
{
  "markitdown": {
    "command": "/path/to/.venv/bin/python",
    "args": ["./markitdown_server/server.py"],
    "cwd": "/Users/syedraza/mcp-local"
  }
}
```

✅ **Integration Points:**
- VS Code with GitHub Copilot Chat
- Claude Desktop
- Any MCP-compatible client

### How to Use MCP Server:

**1. Through VS Code Copilot Chat:**
```
@workspace Convert this PDF to markdown: /path/to/document.pdf
@workspace What formats does markitdown support?
@workspace Convert this webpage: https://example.com
```

**2. Through MCP Inspector:**
```bash
npx @modelcontextprotocol/inspector \
  /path/to/.venv/bin/python \
  /path/to/markitdown_server/server.py
```

**3. Direct Execution (STDIO mode):**
```bash
python markitdown_server/server.py
# Server waits for MCP protocol messages on stdin
```

---

## 2. Web Server Implementation ❌

**File:** `markitdown_server/web_server.py`

### NOT an MCP Server

```python
from fastapi import FastAPI  # ← Regular FastAPI, NOT FastMCP

# Regular FastAPI application
app = FastAPI(
    title="MarkItDown Web Service",
    description="Upload documents and convert them to Markdown"
)

# HTTP REST endpoints (not MCP tools)
@app.post("/convert")
async def convert_file(file: UploadFile):
    """HTTP endpoint, not MCP tool"""
    # ... implementation

@app.get("/")
async def home():
    """Serves HTML page"""
    # ... implementation
```

### Why It's NOT MCP:

❌ **Uses FastAPI, not FastMCP**
- Standard HTTP REST API
- Browser-based interface
- No MCP protocol communication

❌ **HTTP Endpoints (not MCP tools):**
- `POST /convert` - Upload endpoint
- `GET /download/{filename}` - Download endpoint
- `GET /api/formats` - API endpoint

❌ **Different Purpose:**
- Designed for human users with browsers
- Drag & drop file upload
- Visual interface
- Direct HTTP communication

### How to Use Web Server:

```bash
python markitdown_server/web_server.py
# Opens HTTP server on http://localhost:8000
```

Then visit http://localhost:8000 in your browser.

---

## 3. File Watcher Service ❌

**File:** `markitdown_server/watcher_service.py`

### NOT an MCP Server

```python
from watchdog.observers import Observer  # ← File system monitoring

# Standalone service, no protocol
class MarkItDownHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Triggered by file system events"""
        # ... conversion logic
```

### Why It's NOT MCP:

❌ **Standalone Service**
- Monitors file system for changes
- No client-server communication
- No protocol implementation

❌ **Automated Processing:**
- Watches directory for new files
- Automatically converts them
- No API or tool exposure

### How to Use File Watcher:

```bash
python markitdown_server/watcher_service.py
# Monitors /Users/syedraza/Documents/markitdown
# Auto-converts any files dropped there
```

---

## Architecture Comparison

### MCP Server (server.py)
```
┌─────────────────┐
│  AI Assistant   │ (VS Code Copilot, Claude)
│  (MCP Client)   │
└────────┬────────┘
         │ MCP Protocol (STDIO)
         │
┌────────▼────────┐
│  FastMCP Server │ (server.py)
│  - Tools        │
│  - Resources    │
│  - Prompts      │
└────────┬────────┘
         │
┌────────▼────────┐
│   MarkItDown    │
│    Library      │
└─────────────────┘
```

### Web Server (web_server.py)
```
┌─────────────────┐
│   Web Browser   │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│ FastAPI Server  │ (web_server.py)
│  - Endpoints    │
│  - HTML UI      │
└────────┬────────┘
         │
┌────────▼────────┐
│   MarkItDown    │
│    Library      │
└─────────────────┘
```

### File Watcher (watcher_service.py)
```
┌─────────────────┐
│  File System    │
│   /Documents    │
└────────┬────────┘
         │ File Events
         │
┌────────▼────────┐
│ Watchdog Service│ (watcher_service.py)
│  - Observer     │
│  - Handler      │
└────────┬────────┘
         │
┌────────▼────────┐
│   MarkItDown    │
│    Library      │
└─────────────────┘
```

---

## Summary

| Feature | MCP Server | Web Server | File Watcher |
|---------|------------|------------|--------------|
| **MCP Protocol** | ✅ Yes | ❌ No | ❌ No |
| **Framework** | FastMCP | FastAPI | Watchdog |
| **Interface** | STDIO | HTTP | File System |
| **Client** | AI Assistants | Web Browsers | Automatic |
| **Use Case** | AI Integration | Human Users | Background Processing |
| **Configuration** | `mcp/config.json` | URL | Directory Path |

---

## When to Use Each?

### Use MCP Server when:
- Integrating with AI assistants (Copilot, Claude)
- Natural language document conversion
- Building AI-powered workflows
- Want tool discovery and structured interaction

### Use Web Server when:
- Need browser-based UI
- Human users uploading files
- Want visual feedback
- Building web applications

### Use File Watcher when:
- Automated batch processing
- Monitor a folder for new documents
- Unattended conversion
- Integration with other file-based workflows

---

## Verifying MCP Implementation

### Check if a server implements MCP:

1. **Look for FastMCP import:**
   ```python
   from fastmcp import FastMCP  # ✅ MCP implementation
   ```

2. **Check for MCP decorators:**
   ```python
   @app.tool()      # ✅ MCP tool
   @app.resource()  # ✅ MCP resource
   @app.prompt()    # ✅ MCP prompt
   ```

3. **Look for STDIO transport:**
   ```python
   app.run()  # ✅ Runs STDIO transport
   ```

4. **Test with MCP Inspector:**
   ```bash
   npx @modelcontextprotocol/inspector python server.py
   # If it works, it's MCP! ✅
   ```

---

## Your Current Setup

✅ **MCP Server**: `/Users/syedraza/mcp-local/markitdown_server/server.py`
- Configured in: `/Users/syedraza/.config/mcp/config.json`
- Accessible through: VS Code GitHub Copilot Chat
- Tools: `convert_file`, `convert_url`, `convert_batch`, `get_supported_formats`

❌ **Web Server**: `/Users/syedraza/mcp-local/markitdown_server/web_server.py`
- Running on: http://localhost:8000
- Regular FastAPI HTTP server
- Browser-based file upload

❌ **File Watcher**: `/Users/syedraza/mcp-local/markitdown_server/watcher_service.py`
- Watches: `/Users/syedraza/Documents/markitdown`
- Standalone background service
- Automatic file conversion
