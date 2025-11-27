# Local MCP Server

Convert documents to Markdown using **MCP protocol** for AI assistants or **Web interface** for manual uploads. Choose the right implementation for your workflow.

---

## 🎯 What You Get

- **📄 MarkItDown Conversion** - Convert PDF, DOCX, XLSX, PPTX, images, and more to Markdown
- **🗄️ Database Access** - Safe SQLite queries through MCP
- **3 Modes** - MCP server, Web UI, or File watcher

---

## 🚀 Quick Start

**Choose your implementation:**

```bash
# Clone and install
git clone https://github.com/majidraza1228/local-mcpserver.git
cd local-mcpserver
python -m venv .venv
source .venv/bin/activate
pip install fastmcp sqlalchemy markitdown watchdog fastapi uvicorn python-multipart
```

**Then:**
- **For AI Assistants (MCP/STDIO)** → See [MCP Setup](#mcp-setup)
- **For API Integration (MCP/HTTP)** → See [MCP HTTP Setup](#mcp-http-setup)
- **For Web Browser** → See [Web Setup](#web-setup)
- **For Automation** → See [File Watcher](#file-watcher)

---

## 📦 What's Inside

| Implementation | Use Case | Protocol | Details |
|---------------|----------|----------|---------|
| **🤖 MCP Server (STDIO)** | AI assistants (Copilot, Claude) | MCP/STDIO | [Setup & Testing →](TESTING_MCP.md) |
| **📡 MCP HTTP Server** | API integration, streaming | MCP/HTTP+SSE | [Complete Guide →](MCP_HTTP_GUIDE.md) |
| **🌐 Web Server** | Browser uploads | HTTP | [Web Guide →](WEB_SERVER_GUIDE.md) |
| **🔄 Streaming Web** | Real-time progress UI | HTTP+SSE | Port 8001 |
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

### MCP HTTP Setup
**For API Integration with Streaming (HTTP + SSE)**

**Start the server:**
```bash
.venv/bin/python markitdown_server/mcp_http_server.py
# Runs on http://localhost:8002
```

**Test it:**
```bash
# List MCP tools
curl http://localhost:8002/mcp/tools

# Convert a file (JSON response)
curl -X POST http://localhost:8002/mcp/call/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/file.pdf"}'

# Convert with streaming (SSE)
curl -N -X POST http://localhost:8002/mcp/stream/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/file.pdf"}'

# Upload file with streaming
curl -N -X POST http://localhost:8002/mcp/upload \
  -F "file=@/path/to/file.pdf"
```

📖 **[Complete MCP HTTP Guide →](MCP_HTTP_GUIDE.md)**

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

**Testing MCP HTTP:**
- 📖 [MCP_HTTP_GUIDE.md](MCP_HTTP_GUIDE.md) - HTTP endpoints, streaming, curl examples

**Testing Web Server:**
- 📖 [WEB_SERVER_GUIDE.md](WEB_SERVER_GUIDE.md) - HTTP endpoints, browser testing, API docs

---

## 🚀 Production Deployment

**MCP STDIO Production:**
- 📖 [TESTING_MCP.md](TESTING_MCP.md#production-deployment) - systemd, Docker, monitoring

**MCP HTTP Production:**
- 📖 [MCP_HTTP_GUIDE.md](MCP_HTTP_GUIDE.md#production-deployment) - systemd, Docker, nginx, security

**Web Production:**
- 📖 [WEB_SERVER_GUIDE.md](WEB_SERVER_GUIDE.md#production-deployment) - nginx, SSL, scaling

---

## 🔧 Troubleshooting

**MCP STDIO Issues:** See [TESTING_MCP.md - Troubleshooting](TESTING_MCP.md#troubleshooting)

**MCP HTTP Issues:** See [MCP_HTTP_GUIDE.md - Troubleshooting](MCP_HTTP_GUIDE.md#troubleshooting)

**Web Issues:** See [WEB_SERVER_GUIDE.md - Troubleshooting](WEB_SERVER_GUIDE.md#troubleshooting)

**Quick Fixes:**
- Import errors: `source .venv/bin/activate && pip install -r requirements.txt`
- VS Code not recognizing MCP: Check `~/.config/mcp/config.json` paths, restart VS Code

---

## 📝 License

MIT License - feel free to use in your projects.

---

## 📖 Resources

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MarkItDown Library](https://github.com/microsoft/markitdown)
- [MCP Implementation Guide](MCP_IMPLEMENTATION_GUIDE.md)
- [MCP HTTP Streaming Guide](MCP_HTTP_GUIDE.md)

---

## 📞 Support

- Open an issue on [GitHub](https://github.com/majidraza1228/local-mcpserver/issues)
- Check [TESTING_MCP.md](TESTING_MCP.md) for MCP STDIO help
- Check [MCP_HTTP_GUIDE.md](MCP_HTTP_GUIDE.md) for MCP HTTP help
- Check [WEB_SERVER_GUIDE.md](WEB_SERVER_GUIDE.md) for web server help
