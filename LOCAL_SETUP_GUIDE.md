# Quick Start Guide for Developers

Step-by-step guide to run the MCP server locally and integrate it with AI assistants.

---

## 🚀 Quick Setup (5 minutes)

### 1. Clone and Install

```bash
# Clone repository
git clone https://github.com/majidraza1228/local-mcpserver.git
cd local-mcpserver

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
pip install fastmcp markitdown fastapi uvicorn python-multipart sqlalchemy watchdog
```

### 2. Test Installation

```bash
# Verify Python and imports
python --version  # Should be 3.10+
python -c "import fastmcp, markitdown, fastapi; print('✅ All imports successful')"
```

---

## 🎯 Choose Your Mode

You have two ways to run the MCP server locally:

### Option A: MCP STDIO (For AI Assistants)
**Use this for:** VS Code Copilot, Claude Desktop, Cline, or any MCP-compatible AI tool

### Option B: HTTP Streaming Server
**Use this for:** Web browser, REST API, Python/JavaScript applications

---

## 🤖 Option A: MCP STDIO (AI Assistants)

### Step 1: Start the MCP Server

```bash
# Make sure you're in the project directory
cd /path/to/local-mcpserver

# Activate virtual environment
source .venv/bin/activate

# Start MCP STDIO server
.venv/bin/python markitdown_server/server.py
```

The server will run and wait for MCP protocol messages via STDIN/STDOUT.

### Step 2: Configure VS Code Copilot

**Location:** `~/.config/mcp/config.json` (macOS/Linux) or `%APPDATA%\mcp\config.json` (Windows)

**Create or edit the file:**

```json
{
  "version": "1.0",
  "servers": {
    "markitdown": {
      "command": "/absolute/path/to/local-mcpserver/.venv/bin/python",
      "args": ["./markitdown_server/server.py"],
      "cwd": "/absolute/path/to/local-mcpserver"
    },
    "database": {
      "command": "/absolute/path/to/local-mcpserver/.venv/bin/python",
      "args": ["./db_server/server.py"],
      "cwd": "/absolute/path/to/local-mcpserver",
      "env": {
        "DB_PATH": "/absolute/path/to/your/database.db"
      }
    }
  }
}
```

**⚠️ Important:** Replace `/absolute/path/to/local-mcpserver` with your actual path!

**Get your absolute path:**
```bash
# In the project directory, run:
pwd
# Copy the output and use it in config.json
```

**Example config with real paths:**
```json
{
  "version": "1.0",
  "servers": {
    "markitdown": {
      "command": "/Users/johndoe/projects/local-mcpserver/.venv/bin/python",
      "args": ["./markitdown_server/server.py"],
      "cwd": "/Users/johndoe/projects/local-mcpserver"
    }
  }
}
```

### Step 3: Restart VS Code

```bash
# Completely quit and restart VS Code
# On macOS: Cmd+Q then reopen
# On Windows/Linux: Close all windows then reopen
```

### Step 4: Test in VS Code

Open VS Code Copilot Chat and try:

```
@workspace List available MCP tools

@workspace Convert /path/to/document.pdf to markdown

@workspace What file formats can you convert?

@workspace Convert https://github.com/microsoft/markitdown to markdown
```

### Step 5: Configure Claude Desktop (Optional)

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "/absolute/path/to/local-mcpserver/.venv/bin/python",
      "args": ["./markitdown_server/server.py"],
      "cwd": "/absolute/path/to/local-mcpserver"
    }
  }
}
```

**Restart Claude Desktop** and test with:
```
Can you list the available MCP tools?
Convert this file to markdown: /path/to/file.pdf
```

---

## 🌐 Option B: HTTP Streaming Server

### Step 1: Start the HTTP Server

```bash
# Navigate to project directory
cd /path/to/local-mcpserver

# Activate virtual environment
source .venv/bin/activate

# Start HTTP streaming server
./markitdown_server/start_http_streaming.sh

# Server starts on http://localhost:8080
```

You'll see:
```
🚀 Starting MarkItDown HTTP Streaming Server...
📡 MCP Tools + Web UI + SSE Streaming - All in One
🌐 Server: http://localhost:8080

✨ Features:
   • Web UI for file uploads
   • MCP tools accessible via HTTP API
   • Real-time streaming progress (SSE)
   • 4 MCP tools: convert_file, convert_url, convert_batch, get_supported_formats

Press Ctrl+C to stop
```

### Step 2: Access the Web UI

```bash
# Open in browser
open http://localhost:8080  # macOS
# OR
xdg-open http://localhost:8080  # Linux
# OR just visit http://localhost:8080 in any browser
```

**Web UI Features:**
- 📤 Drag-and-drop file uploads
- 📊 Real-time progress bar
- 💾 Download converted Markdown
- 📚 Built-in API documentation tab

### Step 3: Test the API

**List available tools:**
```bash
curl http://localhost:8080/api/tools
```

**Get supported formats:**
```bash
curl http://localhost:8080/api/formats
```

**Convert a local file:**
```bash
curl -X POST http://localhost:8080/api/call/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/absolute/path/to/document.pdf"}'
```

**Upload and convert with streaming:**
```bash
curl -N -X POST http://localhost:8080/api/stream/convert \
  -F "file=@/path/to/document.pdf"
```

**Convert a URL:**
```bash
curl -X POST http://localhost:8080/api/call/convert_url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/page"}'
```

**Batch convert multiple files:**
```bash
curl -X POST http://localhost:8080/api/call/convert_batch \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/path/1.pdf", "/path/2.docx", "/path/3.xlsx"]}'
```

---

## 💻 Communicate with MCP Server (Code Examples)

### Python Client

```python
import requests
import json

# Base URL for the HTTP server
BASE_URL = "http://localhost:8080"

# 1. List available tools
response = requests.get(f"{BASE_URL}/api/tools")
tools = response.json()
print("Available tools:", tools)

# 2. Convert a file (simple JSON response)
response = requests.post(
    f"{BASE_URL}/api/call/convert_file",
    json={"path": "/path/to/document.pdf"}
)
result = response.json()
markdown_content = result["result"]
print(markdown_content)

# 3. Upload and convert with streaming progress
def convert_with_progress(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/stream/convert",
            files={'file': f},
            stream=True
        )
        
        for line in response.iter_lines():
            if line.startswith(b'data: '):
                data = json.loads(line[6:])
                
                if data['type'] == 'progress':
                    print(f"Progress: {data['percent']}% - {data['message']}")
                elif data['type'] == 'complete':
                    print("Conversion complete!")
                    return data['content']
                elif data['type'] == 'error':
                    print(f"Error: {data['message']}")
                    return None

# Usage
markdown = convert_with_progress("/path/to/document.pdf")
print(markdown)

# 4. Convert URL
response = requests.post(
    f"{BASE_URL}/api/call/convert_url",
    json={"url": "https://github.com/microsoft/markitdown"}
)
result = response.json()
print(result["result"])

# 5. Batch convert
response = requests.post(
    f"{BASE_URL}/api/call/convert_batch",
    json={"paths": ["/path/1.pdf", "/path/2.docx"]}
)
results = response.json()["result"]
for path, content in results.items():
    print(f"\n{path}:\n{content[:200]}...")
```

### JavaScript/Node.js Client

```javascript
// Install: npm install node-fetch form-data

const fetch = require('node-fetch');
const FormData = require('form-data');
const fs = require('fs');

const BASE_URL = 'http://localhost:8080';

// 1. List available tools
async function listTools() {
  const response = await fetch(`${BASE_URL}/api/tools`);
  const tools = await response.json();
  console.log('Available tools:', tools);
  return tools;
}

// 2. Convert a file (simple)
async function convertFile(filePath) {
  const response = await fetch(`${BASE_URL}/api/call/convert_file`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: filePath })
  });
  
  const result = await response.json();
  return result.result;
}

// 3. Upload and convert with streaming
async function convertWithStreaming(filePath) {
  const formData = new FormData();
  formData.append('file', fs.createReadStream(filePath));
  
  const response = await fetch(`${BASE_URL}/api/stream/convert`, {
    method: 'POST',
    body: formData
  });
  
  const reader = response.body;
  let content = '';
  
  reader.on('data', (chunk) => {
    const text = chunk.toString();
    const lines = text.split('\n\n');
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        
        if (data.type === 'progress') {
          console.log(`Progress: ${data.percent}% - ${data.message}`);
        } else if (data.type === 'complete') {
          console.log('Conversion complete!');
          content = data.content;
        }
      }
    }
  });
  
  return new Promise((resolve) => {
    reader.on('end', () => resolve(content));
  });
}

// 4. Convert URL
async function convertUrl(url) {
  const response = await fetch(`${BASE_URL}/api/call/convert_url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });
  
  const result = await response.json();
  return result.result;
}

// Usage
(async () => {
  await listTools();
  
  const markdown = await convertFile('/path/to/document.pdf');
  console.log(markdown);
  
  const urlContent = await convertUrl('https://example.com');
  console.log(urlContent);
})();
```

### Browser JavaScript

```html
<!DOCTYPE html>
<html>
<head>
    <title>MCP Client Test</title>
</head>
<body>
    <h1>MCP Server Test</h1>
    
    <input type="file" id="fileInput">
    <button onclick="uploadFile()">Upload & Convert</button>
    
    <div id="progress"></div>
    <pre id="result"></pre>
    
    <script>
        const BASE_URL = 'http://localhost:8080';
        
        // Upload and convert with progress
        async function uploadFile() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Please select a file');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch(`${BASE_URL}/api/stream/convert`, {
                method: 'POST',
                body: formData
            });
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\n\n');
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = JSON.parse(line.slice(6));
                        
                        if (data.type === 'progress') {
                            document.getElementById('progress').textContent = 
                                `${data.percent}% - ${data.message}`;
                        } else if (data.type === 'complete') {
                            document.getElementById('result').textContent = data.content;
                            document.getElementById('progress').textContent = 'Complete!';
                        }
                    }
                }
            }
        }
        
        // Test API on page load
        async function testAPI() {
            // List tools
            const toolsResponse = await fetch(`${BASE_URL}/api/tools`);
            const tools = await toolsResponse.json();
            console.log('Available tools:', tools);
            
            // Get formats
            const formatsResponse = await fetch(`${BASE_URL}/api/formats`);
            const formats = await formatsResponse.json();
            console.log('Supported formats:', formats);
        }
        
        testAPI();
    </script>
</body>
</html>
```

---

## 🔧 Troubleshooting

### Issue: VS Code doesn't recognize MCP server

**Solution:**
1. Check config file location:
   ```bash
   # macOS/Linux
   ls -la ~/.config/mcp/config.json
   
   # Windows
   dir %APPDATA%\mcp\config.json
   ```

2. Verify paths are absolute (not relative):
   ```bash
   # Get absolute path
   cd /path/to/local-mcpserver
   pwd
   # Use this full path in config.json
   ```

3. Check JSON syntax:
   ```bash
   # Validate JSON
   cat ~/.config/mcp/config.json | python -m json.tool
   ```

4. Restart VS Code completely (Cmd+Q on macOS, close all windows on Windows)

### Issue: "Module not found" error

**Solution:**
```bash
# Activate venv first
source .venv/bin/activate

# Reinstall dependencies
pip install fastmcp markitdown fastapi uvicorn python-multipart
```

### Issue: Port 8080 already in use

**Solution:**
```bash
# Find process using port 8080
lsof -i :8080

# Kill the process
kill -9 <PID>

# Or change port in http_streaming_server.py (last line)
# Change: uvicorn.run(app, host="0.0.0.0", port=8080)
# To: uvicorn.run(app, host="0.0.0.0", port=8081)
```

### Issue: Permission denied on startup script

**Solution:**
```bash
chmod +x markitdown_server/start_http_streaming.sh
```

---

## 📚 Available MCP Tools

The server provides **4 MCP tools**:

1. **convert_file** - Convert a local file to Markdown
   ```json
   {"path": "/absolute/path/to/file.pdf"}
   ```

2. **convert_url** - Convert a web page to Markdown
   ```json
   {"url": "https://example.com"}
   ```

3. **convert_batch** - Convert multiple files at once
   ```json
   {"paths": ["/path/1.pdf", "/path/2.docx"]}
   ```

4. **get_supported_formats** - List supported file formats
   ```json
   {}
   ```

---

## 🎯 Quick Reference

### File Locations

| File | Purpose | Location |
|------|---------|----------|
| **MCP Config** | VS Code Copilot | `~/.config/mcp/config.json` |
| **Claude Config** | Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Server Files** | MCP Servers | `markitdown_server/server.py` (STDIO)<br>`markitdown_server/http_streaming_server.py` (HTTP) |

### Commands Cheat Sheet

```bash
# Start STDIO server
.venv/bin/python markitdown_server/server.py

# Start HTTP server
./markitdown_server/start_http_streaming.sh

# Test HTTP API
curl http://localhost:8080/api/tools
curl http://localhost:8080/api/formats

# Convert file via API
curl -X POST http://localhost:8080/api/call/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/file.pdf"}'
```

---

## ✅ Next Steps

1. ✅ **Setup local environment** - Follow [Step 1](#1-clone-and-install)
2. ✅ **Choose mode** - STDIO for AI assistants OR HTTP for API/Web
3. ✅ **Update config** - Edit `~/.config/mcp/config.json` with absolute paths
4. ✅ **Test integration** - Try commands in VS Code Copilot or curl
5. 🚀 **Start building** - Use code examples to integrate into your app

**Need more help?** Check [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for containerization and deployment!
