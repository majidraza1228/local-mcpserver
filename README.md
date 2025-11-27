# Local MCP Server

Convert documents to Markdown using **MCP protocol** for AI assistants or **Web interface** for manual uploads. Choose the right implementation for your workflow.

---

## 🎯 What You Get

- **📄 MarkItDown Conversion** - Convert PDF, DOCX, XLSX, PPTX, images, and more to Markdown
- **🗄️ Database Access** - Safe SQLite queries through MCP
- **3 Modes** - MCP server, Web UI, or File watcher

---

## 🚀 Quick Start

### Automated Setup (Recommended)

```bash
# Clone and run setup script
git clone https://github.com/majidraza1228/local-mcpserver.git
cd local-mcpserver
./setup-local.sh

# That's it! Script will:
# ✓ Create virtual environment
# ✓ Install dependencies
# ✓ Configure MCP for VS Code
# ✓ Test installation
```

### Manual Setup

```bash
# Clone and install
git clone https://github.com/majidraza1228/local-mcpserver.git
cd local-mcpserver
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Then choose your mode:**
- **For AI Assistants (MCP/STDIO)** → [Quick Setup Guide](LOCAL_SETUP_GUIDE.md)
- **For HTTP API + Web UI** → See [HTTP Streaming Setup](#http-streaming-setup)
- **For Automation** → See [File Watcher](#file-watcher)

---

## 📦 What's Inside

| Implementation | Use Case | Protocol | Details |
|---------------|----------|----------|---------|
| **🤖 MCP Server (STDIO)** | AI assistants (Copilot, Claude) | MCP/STDIO | [Setup & Testing →](TESTING_MCP.md) |
| **🌐 HTTP Streaming Server** | Unified: MCP API + Web UI | HTTP+SSE | Port 8080 - All-in-one |
| **📁 File Watcher** | Automated processing | File System | [See below](#file-watcher) |
| **🗄️ Database Server** | SQLite access | MCP/STDIO | [Configuration](#mcp-setup) |

**Supported Formats:** PDF, DOCX, XLSX, PPTX, HTML, TXT, JSON, XML, Images (JPG, PNG, GIF), Audio (WAV)

---

## 🔧 Setup

### MCP Setup (STDIO)
**For AI Assistants (VS Code Copilot, Claude Desktop)**

Edit `~/.config/mcp/config.json`:
```json
{
  "version": "1.0",
  "servers": {
    "markitdown": {
      "command": "/path/to/.venv/bin/python",
      "args": ["./markitdown_server/server.py"],
      "cwd": "/path/to/local-mcpserver"
    }
  }
}
```
**Restart VS Code** and use: `@workspace Convert file.pdf to markdown`

📖 **[Complete MCP STDIO Guide →](TESTING_MCP.md)**

---

### HTTP Streaming Setup
**Unified Server: MCP API + Web UI + Real-time Streaming**

**Start the server:**
```bash
./markitdown_server/start_http_streaming.sh
# Runs on http://localhost:8080
```

**✨ Features:**
- 🌐 **Beautiful Web UI** - Drag-and-drop file uploads with real-time progress
- 📡 **MCP Tools API** - Access all 4 MCP tools via REST endpoints
- ⚡ **SSE Streaming** - Watch conversion progress in real-time
- 🎨 **Tabbed Interface** - Upload tab + API documentation tab
- 📥 **One-Click Download** - Download converted Markdown instantly

**Web Interface:**
```bash
# Open in browser
open http://localhost:8080

# Features:
# - Drag and drop files
# - Real-time conversion progress bar
# - Visual status indicators
# - Download button for results
# - API documentation built-in
```

**API Usage:**
```bash
# List all MCP tools
curl http://localhost:8080/api/tools

# Get supported formats
curl http://localhost:8080/api/formats

# Upload file with streaming (Server-Sent Events)
curl -N -X POST http://localhost:8080/api/stream/convert \
  -F "file=@document.pdf"

# Call MCP tool directly (JSON response)
curl -X POST http://localhost:8080/api/call/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/file.pdf"}'

# Convert URL
curl -X POST http://localhost:8080/api/call/convert_url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Batch conversion
curl -X POST http://localhost:8080/api/call/convert_batch \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/path/1.pdf", "/path/2.docx"]}'
```

**Python Example:**
```python
import requests

# Upload with streaming
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8080/api/stream/convert',
        files={'file': f},
        stream=True
    )
    for line in response.iter_lines():
        if line.startswith(b'data: '):
            print(line.decode())

# Call MCP tool
response = requests.post(
    'http://localhost:8080/api/call/convert_file',
    json={'path': '/path/to/file.pdf'}
)
print(response.json()['result'])
```

---

### Web Setup
**For Browser Interface**

```bash
./markitdown_server/start_web.sh
# Open http://localhost:8000
```

📖 **[Complete Web Guide →](WEB_SERVER_GUIDE.md)**

---

### Streaming Web Setup
**For Real-time Progress UI**

```bash
./markitdown_server/start_streaming.sh
# Open http://localhost:8001
```

---

### File Watcher
**For Automated Processing**

```bash
./markitdown_server/start_watcher.sh
# Drop files in ~/Documents/markitdown
```

---

## 🧪 Testing

### Quick Test (Local Machine)
```bash
./quick_test.sh  # Validates Python, FastMCP, config, tools
```

### Detailed Testing

**Testing MCP STDIO:**
- 📖 [TESTING_MCP.md](TESTING_MCP.md) - MCP Inspector, VS Code Copilot, protocol testing

**Testing HTTP Streaming Server:**
- Open http://localhost:8080 in browser
- Test file upload via drag-and-drop
- Test API endpoints with curl (see [HTTP Streaming Setup](#http-streaming-setup))
- Monitor real-time streaming progress

---

## 🚀 Production Deployment

**MCP STDIO Production:**
- 📖 [TESTING_MCP.md](TESTING_MCP.md#production-deployment) - systemd, Docker, monitoring

**HTTP Streaming Production:**
```bash
# Using systemd
sudo nano /etc/systemd/system/markitdown-http.service

[Unit]
Description=MarkItDown HTTP Streaming Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/local-mcpserver
ExecStart=/path/to/.venv/bin/python markitdown_server/http_streaming_server.py
Restart=always

[Install]
WantedBy=multi-user.target

# Start service
sudo systemctl enable markitdown-http
sudo systemctl start markitdown-http
```

**Using Docker:**
```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY . .
RUN pip install fastmcp markitdown fastapi uvicorn python-multipart
EXPOSE 8080
CMD ["python", "markitdown_server/http_streaming_server.py"]
```

**Using nginx reverse proxy:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 🔧 Troubleshooting

**MCP STDIO Issues:** See [TESTING_MCP.md - Troubleshooting](TESTING_MCP.md#troubleshooting)

**HTTP Streaming Issues:**
- **Port already in use:** Change port in `http_streaming_server.py` (line: `uvicorn.run(app, host="0.0.0.0", port=8080)`)
- **Import errors:** `source .venv/bin/activate && pip install fastmcp markitdown fastapi uvicorn python-multipart`
- **Streaming not working:** Check browser console, ensure using `-N` flag with curl
- **File upload fails:** Check file size limits, temp directory permissions

**Quick Fixes:**
- Import errors: `source .venv/bin/activate && pip install -r requirements.txt`
- VS Code not recognizing MCP: Check `~/.config/mcp/config.json` paths, restart VS Code

---

## 📝 License

MIT License - feel free to use in your projects.

---

## 📖 Resources

- [🚀 Quick Setup Guide - Get Started Fast!](LOCAL_SETUP_GUIDE.md) ⭐
- [Developer Guide - Local to OpenShift](DEVELOPER_GUIDE.md)
- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MarkItDown Library](https://github.com/microsoft/markitdown)
- [MCP Implementation Guide](MCP_IMPLEMENTATION_GUIDE.md)
- [MCP STDIO Testing Guide](TESTING_MCP.md)

---

## 📞 Support

- Open an issue on [GitHub](https://github.com/majidraza1228/local-mcpserver/issues)
- Check [TESTING_MCP.md](TESTING_MCP.md) for MCP STDIO help
- Check [HTTP Streaming Setup](#http-streaming-setup) for HTTP API help
