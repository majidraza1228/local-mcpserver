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
- **For AI Assistants (MCP)** → See [MCP Setup](#mcp-setup)
- **For Web Browser** → See [Web Setup](#web-setup)
- **For Automation** → See [File Watcher](#file-watcher)

---

## 📦 What's Inside

| Implementation | Use Case | Details |
|---------------|----------|----------|
| **🤖 MCP Server** | AI assistants (Copilot, Claude) | [Setup & Testing →](TESTING_MCP.md) |
| **🌐 Web Server** | Browser uploads, REST API | [Setup & Testing →](WEB_SERVER_GUIDE.md) |
| **📁 File Watcher** | Automated batch processing | [See below](#file-watcher) |
| **🗄️ Database Server** | SQLite access via MCP | [Configuration](#mcp-setup) |

**Supported Formats:** PDF, DOCX, XLSX, PPTX, HTML, TXT, JSON, XML, Images (JPG, PNG, GIF), Audio (WAV)

---

## 🔧 Setup

### MCP Setup
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

📖 **[Complete MCP Guide →](TESTING_MCP.md)**

---

### Web Setup
**For Browser Interface**

```bash
./markitdown_server/start_web.sh
# Open http://localhost:8000
```

📖 **[Complete Web Guide →](WEB_SERVER_GUIDE.md)**

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

**Testing MCP Implementation:**
- 📖 [TESTING_MCP.md](TESTING_MCP.md) - MCP Inspector, VS Code Copilot, protocol testing

**Testing Web Server:**
- 📖 [WEB_SERVER_GUIDE.md](WEB_SERVER_GUIDE.md) - HTTP endpoints, browser testing, API docs

---

## 🚀 Production Deployment

**MCP Production:**
- 📖 [TESTING_MCP.md](TESTING_MCP.md#production-deployment) - systemd, Docker, monitoring

**Web Production:**
- 📖 [WEB_SERVER_GUIDE.md](WEB_SERVER_GUIDE.md#production-deployment) - nginx, SSL, scaling

---

## 🔧 Troubleshooting

**MCP Issues:** See [TESTING_MCP.md - Troubleshooting](TESTING_MCP.md#troubleshooting)

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

---

## 📞 Support

- Open an issue on [GitHub](https://github.com/majidraza1228/local-mcpserver/issues)
- Check [TESTING_MCP.md](TESTING_MCP.md) for MCP help
- Check [WEB_SERVER_GUIDE.md](WEB_SERVER_GUIDE.md) for web server help
