# Testing MCP Implementation

This guide shows you how to test your MarkItDown MCP server to verify it's working correctly.

## Quick Test Checklist

- [ ] Test 1: Server starts without errors
- [ ] Test 2: MCP Inspector shows available tools
- [ ] Test 3: VS Code Copilot Chat integration works
- [ ] Test 4: Convert a test file successfully
- [ ] Test 5: MCP configuration is loaded

---

## Method 1: Quick Startup Test ⚡

**Purpose:** Verify the server starts and responds to MCP protocol

```bash
cd /Users/syedraza/mcp-local
source .venv/bin/activate
python markitdown_server/server.py
```

**Expected Output:**
```
╭───────────────────────────────────────────────────────────╮
│                                                           │
│               ▄▀▀ ▄▀█ █▀▀ ▀█▀ █▀▄▀█ █▀▀ █▀█               │
│               █▀  █▀█ ▄▄█  █  █ ▀ █ █▄▄ █▀▀               │
│                                                           │
│                      FastMCP 2.13.1                       │
│                                                           │
│           🖥  Server name: markitdown                      │
│           📦 Transport:   STDIO                           │
│                                                           │
╰───────────────────────────────────────────────────────────╯

INFO: Starting MCP server 'markitdown' with transport 'stdio'
```

**✅ Pass Criteria:** Server starts, shows FastMCP banner, waits for input
**❌ Fail Signs:** Import errors, crashes, HTTP server starts instead

---

## Method 2: MCP Inspector (Interactive Testing) 🔍

**Purpose:** Interactively test all MCP tools with a web UI

### Step 1: Install MCP Inspector
```bash
# No installation needed, runs via npx
```

### Step 2: Launch Inspector
```bash
npx @modelcontextprotocol/inspector \
  /Users/syedraza/mcp-local/.venv/bin/python \
  /Users/syedraza/mcp-local/markitdown_server/server.py
```

### Step 3: Open Web Interface
The inspector will output:
```
MCP Inspector running at http://localhost:5173
```

Open that URL in your browser.

### Step 4: Test Each Tool

**Test convert_file:**
```json
{
  "path": "/Users/syedraza/Documents/test.txt"
}
```

**Test convert_url:**
```json
{
  "url": "https://example.com"
}
```

**Test get_supported_formats:**
```json
{}
```

**Test convert_batch:**
```json
{
  "paths": ["/path/to/file1.txt", "/path/to/file2.pdf"]
}
```

### Expected Results:

**✅ Success Indicators:**
- All 4 tools appear in the tools list
- Each tool shows description and parameters
- Tool execution returns JSON results
- No error messages in console

**❌ Failure Signs:**
- Tools don't appear
- "Connection failed" errors
- Timeout errors
- Python exceptions in terminal

---

## Method 3: VS Code Copilot Chat Testing 🤖

**Purpose:** Test real-world AI assistant integration

### Step 1: Verify Configuration
```bash
cat /Users/syedraza/.config/mcp/config.json
```

Should show:
```json
{
  "markitdown": {
    "command": "/Users/syedraza/mcp-local/.venv/bin/python",
    "args": ["./markitdown_server/server.py"],
    "cwd": "/Users/syedraza/mcp-local"
  }
}
```

### Step 2: Restart VS Code
```bash
# Quit and reopen VS Code completely
# Or use Command Palette: "Developer: Reload Window"
```

### Step 3: Open Copilot Chat
- Press `Cmd+Shift+I` (Mac) or `Ctrl+Shift+I` (Windows/Linux)
- Or click the chat icon in the sidebar

### Step 4: Test Queries

**Test 1: List supported formats**
```
@workspace What file formats does the markitdown server support?
```

**Expected:** Should list PDF, DOCX, XLSX, PPTX, images, audio, etc.

**Test 2: Convert a file**
```
@workspace Convert this file to markdown: /Users/syedraza/Documents/test.pdf
```

**Expected:** Returns markdown content or asks for valid file path

**Test 3: Convert a URL**
```
@workspace Convert this webpage to markdown: https://github.com/microsoft/markitdown
```

**Expected:** Returns markdown version of the webpage

### Troubleshooting VS Code Integration:

**If tools don't appear:**
1. Check MCP config path: `/Users/syedraza/.config/mcp/config.json`
2. Verify Python path is correct in config
3. Restart VS Code completely
4. Check VS Code output panel for MCP errors

**Check MCP logs in VS Code:**
1. Open Command Palette (`Cmd+Shift+P`)
2. Search for "Output"
3. Select "MCP" from dropdown
4. Look for connection/error messages

---

## Method 4: Manual MCP Protocol Testing 🔧

**Purpose:** Low-level MCP protocol verification

### Create Test Script

Create `test_mcp_manual.py`:

```python
#!/usr/bin/env python3
"""Manual MCP protocol test"""

import subprocess
import json
import sys

def test_mcp_server():
    # Start the MCP server
    process = subprocess.Popen(
        ['/Users/syedraza/mcp-local/.venv/bin/python', 
         '/Users/syedraza/mcp-local/markitdown_server/server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send initialize request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    # Send request
    process.stdin.write(json.dumps(init_request) + '\n')
    process.stdin.flush()
    
    # Read response
    response_line = process.stdout.readline()
    print("Response:", response_line)
    
    # Send tools/list request
    tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }
    
    process.stdin.write(json.dumps(tools_request) + '\n')
    process.stdin.flush()
    
    # Read response
    response_line = process.stdout.readline()
    print("Tools:", response_line)
    
    # Cleanup
    process.terminate()
    process.wait()

if __name__ == "__main__":
    test_mcp_server()
```

### Run Test:
```bash
chmod +x test_mcp_manual.py
python test_mcp_manual.py
```

**Expected Output:**
```json
Response: {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05",...}}
Tools: {"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"convert_file",...}]}}
```

---

## Method 5: Create Test Files 📄

**Purpose:** Prepare test files for conversion testing

### Create Test Directory:
```bash
mkdir -p /Users/syedraza/Documents/mcp-test-files
cd /Users/syedraza/Documents/mcp-test-files
```

### Create Test Files:

**1. Simple Text File:**
```bash
cat > test.txt << 'EOF'
# Test Document

This is a test document for MarkItDown MCP server.

## Features
- Bullet point 1
- Bullet point 2

EOF
```

**2. HTML File:**
```bash
cat > test.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body>
<h1>Test Heading</h1>
<p>This is a test paragraph.</p>
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>
</body>
</html>
EOF
```

**3. JSON File:**
```bash
cat > test.json << 'EOF'
{
  "name": "Test Data",
  "version": "1.0",
  "items": [
    {"id": 1, "value": "First"},
    {"id": 2, "value": "Second"}
  ]
}
EOF
```

### Test with MCP Inspector:

1. Start MCP Inspector (Method 2)
2. Use `convert_file` tool with paths:
   - `/Users/syedraza/Documents/mcp-test-files/test.txt`
   - `/Users/syedraza/Documents/mcp-test-files/test.html`
   - `/Users/syedraza/Documents/mcp-test-files/test.json`

---

## Method 6: Check MCP Configuration ⚙️

**Purpose:** Verify MCP server is properly configured

### Check Config File:
```bash
cat /Users/syedraza/.config/mcp/config.json | jq .
```

### Verify Settings:
```bash
# Check if markitdown server is configured
cat /Users/syedraza/.config/mcp/config.json | grep -A 5 "markitdown"
```

### Test Python Path:
```bash
# Verify Python executable works
/Users/syedraza/mcp-local/.venv/bin/python --version

# Verify FastMCP is installed
/Users/syedraza/mcp-local/.venv/bin/python -c "import fastmcp; print(fastmcp.__version__)"

# Verify MarkItDown is installed
/Users/syedraza/mcp-local/.venv/bin/python -c "import markitdown; print('MarkItDown OK')"
```

---

## Common Issues & Solutions 🔧

### Issue 1: "ModuleNotFoundError: No module named 'fastmcp'"

**Solution:**
```bash
cd /Users/syedraza/mcp-local
source .venv/bin/activate
pip install fastmcp markitdown
```

### Issue 2: Server starts but tools don't appear

**Check:**
1. Verify `@app.tool()` decorators are present in code
2. Check server output for errors
3. Use MCP Inspector to see tool list

### Issue 3: VS Code doesn't recognize MCP server

**Solution:**
1. Check config path: `/Users/syedraza/.config/mcp/config.json`
2. Verify full Python path in config
3. Restart VS Code completely
4. Check VS Code MCP extension is installed

### Issue 4: "Connection refused" or timeout errors

**Check:**
1. Server is running (check Activity Monitor)
2. No firewall blocking localhost
3. Port 8000 not already in use (for web server)

---

## Success Criteria Checklist ✅

Your MCP implementation is working correctly if:

- [ ] Server starts with FastMCP banner
- [ ] MCP Inspector shows 4 tools: `convert_file`, `convert_url`, `convert_batch`, `get_supported_formats`
- [ ] Each tool has proper description and parameters
- [ ] `convert_file` successfully converts test files
- [ ] `convert_url` converts web pages to markdown
- [ ] `get_supported_formats` returns list of 12+ formats
- [ ] VS Code Copilot Chat recognizes the server
- [ ] Chat queries return proper responses
- [ ] No Python errors in terminal
- [ ] Configuration in `/Users/syedraza/.config/mcp/config.json` is correct

---

## Quick Test Script 🚀

Save as `quick_test.sh`:

```bash
#!/bin/bash

echo "==================================="
echo "MCP Server Quick Test"
echo "==================================="
echo ""

echo "Test 1: Check Python environment..."
/Users/syedraza/mcp-local/.venv/bin/python --version
if [ $? -eq 0 ]; then
    echo "✅ Python OK"
else
    echo "❌ Python FAILED"
    exit 1
fi

echo ""
echo "Test 2: Check FastMCP installation..."
/Users/syedraza/mcp-local/.venv/bin/python -c "import fastmcp; print('FastMCP version:', fastmcp.__version__)"
if [ $? -eq 0 ]; then
    echo "✅ FastMCP OK"
else
    echo "❌ FastMCP FAILED"
    exit 1
fi

echo ""
echo "Test 3: Check MarkItDown installation..."
/Users/syedraza/mcp-local/.venv/bin/python -c "import markitdown; print('MarkItDown OK')"
if [ $? -eq 0 ]; then
    echo "✅ MarkItDown OK"
else
    echo "❌ MarkItDown FAILED"
    exit 1
fi

echo ""
echo "Test 4: Check MCP config exists..."
if [ -f "/Users/syedraza/.config/mcp/config.json" ]; then
    echo "✅ MCP config exists"
    cat /Users/syedraza/.config/mcp/config.json | grep "markitdown" > /dev/null
    if [ $? -eq 0 ]; then
        echo "✅ markitdown server configured"
    else
        echo "❌ markitdown server NOT configured"
    fi
else
    echo "❌ MCP config NOT found"
fi

echo ""
echo "Test 5: Start server (5 seconds)..."
timeout 5 /Users/syedraza/mcp-local/.venv/bin/python /Users/syedraza/mcp-local/markitdown_server/server.py > /tmp/mcp_test.log 2>&1 &
PID=$!
sleep 2

if ps -p $PID > /dev/null; then
    echo "✅ Server started successfully"
    kill $PID 2>/dev/null
else
    echo "❌ Server FAILED to start"
    cat /tmp/mcp_test.log
    exit 1
fi

echo ""
echo "==================================="
echo "✅ All tests passed!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Run MCP Inspector: npx @modelcontextprotocol/inspector /Users/syedraza/mcp-local/.venv/bin/python /Users/syedraza/mcp-local/markitdown_server/server.py"
echo "2. Test in VS Code Copilot Chat"
```

### Run Quick Test:
```bash
chmod +x quick_test.sh
./quick_test.sh
```

---

## Getting Help 🆘

If tests fail, check:

1. **Error logs:** Look for Python tracebacks
2. **VS Code Output:** MCP panel shows connection errors
3. **Config file:** Verify paths are absolute and correct
4. **Dependencies:** Run `pip list | grep -E "fastmcp|markitdown"`
5. **MCP Implementation Guide:** See `MCP_IMPLEMENTATION_GUIDE.md`

**Still stuck?** Compare your `server.py` with the template:
- Must use `from fastmcp import FastMCP`
- Must use `@app.tool()` decorators
- Must call `app.run()` at the end
