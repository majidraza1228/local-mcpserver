# Local MCP Server

A collection of Model Context Protocol (MCP) servers and utilities for document conversion and database access. Features multiple implementation modes for different use cases.

---

## 📑 Table of Contents

- [Quick Start](#quick-start)
- [Available Implementations](#available-implementations)
- [Servers Overview](#servers-overview)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)

---

## 🚀 Quick Start

### For AI Assistant Integration (MCP)
```bash
# Install and configure for VS Code Copilot Chat
git clone https://github.com/majidraza1228/local-mcpserver.git
cd local-mcpserver
python -m venv .venv
source .venv/bin/activate
pip install fastmcp sqlalchemy markitdown

# Configure MCP servers (see detailed guide below)
```

### For Web Interface
```bash
# Start the web server for browser-based uploads
./markitdown_server/start_web.sh
# Open http://localhost:8000
```

### For Automated Processing
```bash
# Start file watcher for automatic conversion
./markitdown_server/start_watcher.sh
# Drop files in ~/Documents/markitdown
```

---

## 🎯 Available Implementations

This project provides **three different ways** to use MarkItDown document conversion:

| Mode | Interface | Protocol | Best For | Guide |
|------|-----------|----------|----------|-------|
| **MCP Server** ✅ | AI Assistants | MCP/STDIO | VS Code Copilot, Claude Desktop | [Testing Guide](TESTING_MCP.md) |
| **Web Server** 🌐 | Browser UI | HTTP/REST | Manual uploads, human users | [Web Guide](WEB_SERVER_GUIDE.md) |
| **File Watcher** 📁 | Automated | File System | Background processing, batch jobs | [See Below](#file-watcher-mode) |

**Plus:** Database MCP Server for SQLite access

---

## 📦 Servers Overview

### 1. MarkItDown MCP Server ✅
**File:** `markitdown_server/server.py`

**MCP Implementation** using FastMCP framework for AI assistant integration.

**Tools:**
- `convert_file(path)` - Convert local documents
- `convert_url(url)` - Convert web pages
- `convert_batch(paths)` - Batch processing
- `get_supported_formats()` - List supported formats

**Supported Formats:** PDF, DOCX, XLSX, PPTX, HTML, TXT, JSON, XML, JPG, PNG, GIF, WAV

**Integration:**
- ✅ VS Code with GitHub Copilot Chat
- ✅ Claude Desktop
- ✅ Any MCP-compatible client

**Usage:**
```bash
@workspace Convert document.pdf to markdown
@workspace What formats are supported?
```

📖 **[Testing & Integration Guide →](TESTING_MCP.md)**

---

### 2. MarkItDown Web Server 🌐
**File:** `markitdown_server/web_server.py`

**FastAPI HTTP Server** (NOT MCP) with beautiful drag-and-drop UI.

**Features:**
- 🎨 Beautiful web interface
- 📤 Drag & drop file upload
- 📥 Instant markdown download
- 🔄 Real-time conversion status
- 📊 REST API endpoints

**Usage:**
```bash
python markitdown_server/web_server.py
# Open http://localhost:8000
```

📖 **[Complete Web Server Guide →](WEB_SERVER_GUIDE.md)**

---

### 3. MarkItDown File Watcher 📁
**File:** `markitdown_server/watcher_service.py`

**Automated Service** (NOT MCP) that monitors a folder and auto-converts files.

**How It Works:**
1. Drop files → `/Users/syedraza/Documents/markitdown`
2. Auto-converts to Markdown
3. Saves to → `/Users/syedraza/Documents/markitdown/converted`
4. Moves originals → `/Users/syedraza/Documents/markitdown/processed`

**Usage:**
```bash
./markitdown_server/start_watcher.sh
```

---

### 4. Database MCP Server ✅
**File:** `db_server/server.py`

**MCP Implementation** for safe SQLite database access.

**Tools:**
- `db_tables()` - List all tables
- `db_preview(table, limit)` - Preview table data
- `db_query(sql, params, max_rows)` - Execute queries

**Features:**
- ✅ Read-only mode by default
- ✅ Parameterized queries
- ✅ Schema inspection
- ✅ Query result limiting

**Usage:**
```bash
@workspace Show all tables in the database
@workspace Query users table
```

---

## 🏁 Getting Started

## 🏁 Getting Started

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/majidraza1228/local-mcpserver.git
cd local-mcpserver

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install fastmcp sqlalchemy markitdown watchdog fastapi uvicorn python-multipart
```

### Configuration for VS Code + Copilot

Create or edit `/Users/yourusername/.config/mcp/config.json`:

```json
{
  "version": "1.0",
  "servers": {
    "markitdown": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["./markitdown_server/server.py"],
      "cwd": "/absolute/path/to/local-mcpserver"
    },
    "db": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["./db_server/server.py"],
      "env": {
        "DB_DSN": "sqlite+pysqlite:///./app.db",
        "DB_READONLY": "1"
      },
      "cwd": "/absolute/path/to/local-mcpserver"
    }
  }
}
```

**Restart VS Code** and start using with Copilot Chat!

---

## 📚 Documentation

| Guide | Description | Link |
|-------|-------------|------|
| **MCP Testing** | How to test MCP implementation with Inspector & Copilot | [TESTING_MCP.md](TESTING_MCP.md) |
| **Web Server** | Complete guide for browser-based interface | [WEB_SERVER_GUIDE.md](WEB_SERVER_GUIDE.md) |
| **MCP vs Non-MCP** | Understanding implementation differences | [MCP_IMPLEMENTATION_GUIDE.md](MCP_IMPLEMENTATION_GUIDE.md) |

---

## 🧪 Testing

### Quick Test
```bash
./quick_test.sh
```

Validates: Python environment, FastMCP, MarkItDown, config, and MCP tools.

### Detailed Testing

**MCP Server Testing:**
- 📖 See [TESTING_MCP.md](TESTING_MCP.md) for comprehensive guide
- Methods: MCP Inspector, VS Code Copilot, Manual Protocol Testing

**Web Server Testing:**
- 📖 See [WEB_SERVER_GUIDE.md](WEB_SERVER_GUIDE.md) for complete guide
- Start server and test at http://localhost:8000

---

## 📁 Project Structure

```
local-mcpserver/
├── markitdown_server/
│   ├── server.py              # ✅ MCP server implementation
│   ├── web_server.py          # 🌐 FastAPI web interface
│   ├── watcher_service.py     # 📁 File watcher service
│   ├── start_web.sh          # Web server launcher
│   └── start_watcher.sh      # File watcher launcher
├── db_server/
│   └── server.py              # ✅ MCP database server
├── MCP_IMPLEMENTATION_GUIDE.md  # Understanding MCP vs non-MCP
├── TESTING_MCP.md               # MCP testing guide
├── WEB_SERVER_GUIDE.md          # Web server complete guide
├── quick_test.sh                # Automated test script
└── README.md                    # This file
```

---

## 🎯 Use Cases

**MCP Mode** (AI Integration):
- Natural language document conversion with Copilot
- AI-assisted database queries
- Automated workflows with AI assistants

**Web Mode** (Browser):
- Manual file uploads and conversions
- Quick one-off document processing
- User-friendly interface for non-developers

**Watcher Mode** (Automated):
- Batch processing workflows
- Unattended document conversion
- Integration with file-based workflows

---

## 🔧 Troubleshooting

### MCP Server Issues
See [TESTING_MCP.md](TESTING_MCP.md) - Troubleshooting section

### Web Server Issues
See [WEB_SERVER_GUIDE.md](WEB_SERVER_GUIDE.md) - Troubleshooting section

### Common Issues

**Import Errors:**
```bash
source .venv/bin/activate
pip install fastmcp sqlalchemy markitdown
```

**VS Code Not Recognizing MCP:**
1. Check config path: `/Users/yourusername/.config/mcp/config.json`
2. Verify absolute paths in config
3. Restart VS Code completely

---

## 📝 License

MIT License - feel free to use in your projects.

---

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

---

## 📖 Resources

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MarkItDown Library](https://github.com/microsoft/markitdown)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)

---

## 📞 Support

- Open an issue on GitHub
- Check [TESTING_MCP.md](TESTING_MCP.md) for MCP help
- Check [WEB_SERVER_GUIDE.md](WEB_SERVER_GUIDE.md) for web server help
- Review [MCP_IMPLEMENTATION_GUIDE.md](MCP_IMPLEMENTATION_GUIDE.md) for architecture details

Using pipenv (recommended):
```bash
pipenv install
pipenv shell
```

Or using pip:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or .venv\Scripts\activate on Windows

pip install fastmcp sqlalchemy markitdown mcp
```

### 3. Configure Environment Variables (Optional for Database)

Create a `.env` file in the root directory:

```bash
# Database Configuration
DB_DSN=sqlite+pysqlite:///./app.db
DB_READONLY=1
DB_MAX_ROWS=1000
```

**Note:** Never commit your `.env` file to git. It's already included in `.gitignore`.

## Servers

### 1. Markitdown Server (`markitdown_server/server.py`)

Convert documents and web pages to clean Markdown format.

#### Features
- Document conversion (PDF, DOCX, XLSX, PPTX)
- Web page scraping and conversion
- Image OCR (extract text from images)
- Audio transcription
- Batch file processing
- 12+ supported file formats

#### Tools
- `convert_file(path)` - Convert a local file to Markdown
- `convert_url(url)` - Convert a web page to Markdown
- `convert_batch(paths)` - Convert multiple files at once
- `get_supported_formats()` - List all supported file formats

#### Supported Formats
- **Documents**: PDF, DOCX, XLSX, PPTX, TXT, HTML
- **Data**: JSON, XML
- **Images**: JPG, PNG, GIF (with OCR)
- **Audio**: WAV (with transcription)
- **Web**: Any HTTP/HTTPS URL

#### Usage
```bash
python markitdown_server/server.py
```

#### Example Usage
```python
# Convert a PDF document
convert_file("/path/to/document.pdf")

# Convert a webpage
convert_url("https://example.com/article")

# Batch convert multiple files
convert_batch(["/path/to/file1.pdf", "/path/to/file2.docx"])

# Check supported formats
get_supported_formats()
```

### 2. Database Server (`db_server/server.py`)

Provides safe SQLite database access with configurable read/write permissions.

#### Features
- Schema inspection via resource endpoint
- Table listing
- Row preview with pagination
- Parameterized SQL queries with safety controls

#### Tools
- `db_tables()` - List all tables in the database
- `db_preview(table, limit)` - Preview first N rows from a table
- `db_query(sql, params, max_rows)` - Execute parameterized SQL queries

#### Resources
- `resource://db/schema` - Database schema information in markdown format

#### Usage
```bash
python db_server/server.py
```

#### Configuration
- `DB_DSN` - Database connection string (default: `sqlite+pysqlite:///./app.db`)
- `DB_READONLY` - Enable read-only mode (default: `1`)
- `DB_MAX_ROWS` - Maximum rows returned per query (default: `1000`)

## Running the Servers

# List open issues
list_issues(owner="majidraza1228", repo="local-mcpserver", state="open", limit=20)

# Search repositories
search_repos(query="machine learning python", limit=10)

# Create a new branch
create_branch(owner="majidraza1228", repo="local-mcpserver", branch_name="feature/new-feature", from_branch="master")

# Create or update a file
create_or_update_file(
    owner="majidraza1228",
    repo="local-mcpserver",
    path="README.md",
    content="# Updated content",
    message="Update README",
    branch="feature/new-feature"
)

# Create a pull request
create_pull_request(
    owner="majidraza1228",
    repo="local-mcpserver",
    title="Add new feature",
    head="feature/new-feature",
    base="master",
    body="Description of changes"
)
```

#### Complete PR Creation Example

### 3. Markitdown Service

Converts various document formats to markdown. Available in **three implementations**:

- ✅ **MCP Server** (`server.py`) - Model Context Protocol implementation for AI assistants
- ❌ **Web Server** (`web_server.py`) - FastAPI HTTP server with browser UI (NOT MCP)
- ❌ **File Watcher** (`watcher_service.py`) - Automated file monitoring service (NOT MCP)

> **Note:** Only `server.py` implements the MCP protocol. The web and watcher services are alternative interfaces to the same MarkItDown conversion functionality.

---

---

#### A. MCP Server Mode ✅ (AI Assistant Integration)

**File:** `markitdown_server/server.py`

**MCP Implementation:** Uses FastMCP framework with MCP protocol (STDIO transport)

**Exposes MCP Tools:**
- `convert_file(path)` - Convert local files
- `convert_url(url)` - Convert web pages  
- `convert_batch(paths)` - Batch conversion
- `get_supported_formats()` - List supported formats

**Usage:**
```bash
python markitdown_server/server.py
```

**Integration:**
- VS Code with GitHub Copilot Chat: `@workspace Convert file.pdf to markdown`
- Claude Desktop with MCP
- Any MCP-compatible client

**Why it's MCP:**
```python
from fastmcp import FastMCP  # ← MCP framework
app = FastMCP(name="markitdown", ...)
@app.tool()  # ← MCP tool decorator
```

---

#### B. Web Interface Mode ❌ (Browser Upload - NOT MCP)

**File:** `markitdown_server/web_server.py`

**Implementation:** Regular FastAPI HTTP server (NO MCP protocol)

Beautiful web UI for uploading and converting files:

```bash
# Start the web server
./markitdown_server/start_web.sh

# Or run directly
python markitdown_server/web_server.py
```

Then open http://localhost:8000 in your browser and drag & drop files to convert!

**Features:**
- 🎨 Beautiful drag-and-drop interface
- 📤 Upload files through browser
- 📥 Download converted Markdown files
- 🔄 Real-time conversion status
- 📊 REST API endpoints available

**Why it's NOT MCP:**
```python
from fastapi import FastAPI  # ← Regular FastAPI, not FastMCP
app = FastAPI(...)
@app.post("/convert")  # ← HTTP endpoint, not MCP tool
```

---

#### C. File Watcher Service Mode ❌ (Auto-Convert - NOT MCP)

**File:** `markitdown_server/watcher_service.py`

**Implementation:** Standalone file system monitoring service (NO MCP protocol)

Automatically converts documents dropped into a watched folder:

```bash
# Start the watcher service
./markitdown_server/start_watcher.sh

# Or run directly
python markitdown_server/watcher_service.py
```

**How it works:**
1. Drop files into: `/Users/syedraza/Documents/markitdown`
2. Service automatically converts them to Markdown
3. Converted files saved to: `/Users/syedraza/Documents/markitdown/converted`
4. Original files moved to: `/Users/syedraza/Documents/markitdown/processed`

**Why it's NOT MCP:**
```python
from watchdog.observers import Observer  # ← File system watcher, not MCP
class MarkItDownHandler(FileSystemEventHandler):  # ← Event handler, not MCP tool
```

---

**Supported formats (all modes):** PDF, DOCX, XLSX, PPTX, HTML, TXT, JSON, XML, JPG, PNG, GIF, WAV

> **📖 For detailed comparison, see:** [MCP_IMPLEMENTATION_GUIDE.md](MCP_IMPLEMENTATION_GUIDE.md)

## Running the Servers

Each server runs independently using the STDIO transport protocol for MCP communication.

### Prerequisites
- Ensure virtual environment is activated
- Set environment variables if using database server

### Running Locally

#### Markitdown Server
```bash
# Using full path to venv python
/path/to/local-mcpserver/.venv/bin/python ./markitdown_server/server.py

# Or if venv is activated
python3 ./markitdown_server/server.py
```

#### Database Server
```bash
# Using full path to venv python
/path/to/local-mcpserver/.venv/bin/python ./db_server/server.py

# Or if venv is activated
python3 ./db_server/server.py
```

**Note:** Servers run in STDIO mode and wait for MCP protocol messages. They won't show output until they receive input from an MCP client.

## Using with VS Code & GitHub Copilot

Integrate these servers with VS Code and use GitHub Copilot Chat for natural language interactions:

### Quick Setup

1. Configure `.vscode/settings.json` (see Quick Start section above)
2. Restart VS Code
3. Use Copilot Chat to interact with the servers

### Example Conversations

**For Markitdown:**
```
@workspace Convert this PDF to markdown: /path/to/document.pdf
@workspace Extract text from this image: /path/to/image.jpg
@workspace Convert this webpage: https://example.com
```

**For Database:**
```
@workspace Show me all tables in the database
@workspace Preview the users table
@workspace Query the database for active users
```

## Testing the Servers

### Quick MCP Test

Run the automated test script:

```bash
./quick_test.sh
```

This verifies:
- ✅ Python environment
- ✅ FastMCP installation
- ✅ MarkItDown installation
- ✅ MCP configuration
- ✅ Server file and MCP tools

### Detailed MCP Testing

See **[TESTING_MCP.md](TESTING_MCP.md)** for comprehensive testing guide including:

1. **MCP Inspector** - Interactive tool testing with web UI
2. **VS Code Copilot Chat** - Real AI assistant integration
3. **Manual Protocol Testing** - Low-level MCP verification
4. **Test Files** - Sample documents for conversion testing

### Option 1: Manual Testing

Test the servers manually by running them:

```bash
# Test Markitdown Server
python markitdown_server/server.py
# You should see the FastMCP startup banner

# Test Database Server
python db_server/server.py
# You should see the FastMCP startup banner
```

### Option 2: MCP Inspector (Interactive Testing)

Use the official MCP Inspector for interactive testing:

```bash
# Test Markitdown Server
npx @modelcontextprotocol/inspector \
  /path/to/local-mcpserver/.venv/bin/python \
  /path/to/local-mcpserver/markitdown_server/server.py

# Test Database Server
npx @modelcontextprotocol/inspector \
  /path/to/local-mcpserver/.venv/bin/python \
  /path/to/local-mcpserver/db_server/server.py
```

This opens a web interface where you can:
- View all available tools and resources
- Test tools interactively with custom parameters
- See real-time request/response logs

### Using with MCP Clients

These servers are designed to work with MCP-compatible clients. The servers communicate via standard input/output (STDIO transport).

Example client configuration (for Claude Desktop or similar):
```json
{
  "mcpServers": {
    "database": {
      "command": "/path/to/local-mcpserver/.venv/bin/python",
      "args": ["/path/to/local-mcpserver/db_server/server.py"],
      "env": {
        "DB_DSN": "sqlite+pysqlite:///./app.db",
        "DB_READONLY": "1"
      }
    },
    "markitdown": {
      "command": "/path/to/local-mcpserver/.venv/bin/python",
      "args": ["/path/to/local-mcpserver/markitdown_server/server.py"]
    }
  }
}
```

## Project Structure

```
local-mcpserver/
├── db_server/
│   └── server.py              # Database MCP server
├── markitdown_server/
│   └── server.py              # Markitdown conversion server
├── .env                       # Environment variables (optional)
├── .gitignore                 # Git ignore file
├── Pipfile                    # Python dependencies (pipenv)
├── Pipfile.lock              # Locked dependencies
└── README.md                  # This file
```

## Dependencies

- **fastmcp** (>=2.13.1) - FastMCP framework for building MCP servers
- **sqlalchemy** - Database toolkit and ORM
- **markitdown** - Document conversion library

## Security Considerations

### Database Server
- Read-only mode is enabled by default (`DB_READONLY=1`)
- Write operations (INSERT, UPDATE, DELETE, etc.) are blocked in read-only mode
- Query results are capped to prevent memory issues
- Use parameterized queries to prevent SQL injection

## Troubleshooting

### Import Errors
If you get `ModuleNotFoundError`, ensure you're using the virtual environment:
```bash
# Check which Python is being used
which python

# Should point to .venv/bin/python
# If not, activate the virtual environment
source .venv/bin/activate
```

### Database Connection Issues
- Verify the `DB_DSN` connection string is correct
- Check file permissions for SQLite database file
- Ensure SQLite driver is installed: `pip install sqlalchemy`

### Server Not Starting
Ensure all dependencies are installed:
```bash
pip install fastmcp sqlalchemy markitdown
```

## Development

### Adding New Tools

To add a new tool to any server:

```python
@app.tool(description="Your tool description")
def your_tool_name(param1: str, param2: int = 10):
    """Tool documentation."""
    # Your implementation
    return {"result": "data"}
```

### Adding New Resources

To add a new resource:

```python
@app.resource(uri="resource://your/path", mime_type="text/plain")
def your_resource():
    """Resource documentation."""
    return "resource content"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

## License

MIT License - feel free to use this code for your projects.

## Resources

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [MarkItDown Documentation](https://github.com/microsoft/markitdown)
- [VS Code MCP Configuration](https://modelcontextprotocol.io/clients/vscode)

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the FastMCP documentation

## Changelog

### v1.0.0 (2024-11-24)
- Initial release
- Database server with SQLite support
- Markitdown server for document conversion to Markdown
