# Traditional MCP Setup Guide

## 🤖 What is Traditional MCP?

Traditional MCP uses **STDIO protocol** - exactly how VS Code Copilot and Claude Desktop communicate with MCP servers:

- ✅ Text-based JSON-RPC 2.0 protocol
- ✅ Communication via STDIN/STDOUT
- ✅ No HTTP, no web, just pure protocol
- ✅ Same method AI assistants use

---

## 📋 Setup Steps

### 1. Configure VS Code Copilot

Edit `~/.config/mcp/config.json`:

```json
{
  "version": "1.0",
  "servers": {
    "markitdown": {
      "command": "/Users/syedraza/mcp-local/.venv/bin/python",
      "args": ["./markitdown_server/server.py"],
      "cwd": "/Users/syedraza/mcp-local",
      "description": "Convert PDF, DOCX, XLSX to Markdown"
    }
  }
}
```

**⚠️ Important:** Use YOUR absolute paths!

Get your path:
```bash
cd /Users/syedraza/mcp-local
pwd  # Use this output
```

### 2. Restart VS Code

Completely quit and restart VS Code (Cmd+Q on macOS).

### 3. Test in VS Code Copilot

```
@workspace List available MCP tools

@workspace Convert /path/to/document.pdf to markdown

@workspace What file formats can you convert?

@workspace Convert https://example.com to markdown
```

---

## 🧪 Manual Testing (Without VS Code)

### Test 1: Using MCP Inspector

```bash
# Install MCP Inspector
npx @modelcontextprotocol/inspector /Users/syedraza/mcp-local/.venv/bin/python markitdown_server/server.py

# Opens browser at http://localhost:6274
# You can test all MCP tools interactively
```

### Test 2: Direct STDIO Communication

The MCP server is running in the background. Here's how to communicate:

```bash
# The server expects JSON-RPC 2.0 messages via STDIN
# But it needs a persistent connection (like VS Code provides)

# That's why we use:
# 1. VS Code Copilot (recommended)
# 2. MCP Inspector (for testing)
# 3. Claude Desktop (alternative AI assistant)
```

---

## 📊 MCP Tools Available

Your server provides 4 MCP tools:

1. **convert_file** - Convert local file to Markdown
   ```
   @workspace Convert /path/to/document.pdf to markdown
   ```

2. **convert_url** - Convert web page to Markdown
   ```
   @workspace Convert https://example.com to markdown
   ```

3. **convert_batch** - Convert multiple files
   ```
   @workspace Convert these files to markdown: file1.pdf, file2.docx
   ```

4. **get_supported_formats** - List supported formats
   ```
   @workspace What file formats can you convert?
   ```

---

## ✅ Verification

After setup, verify it works:

```
1. Open VS Code
2. Open Copilot Chat
3. Type: @workspace List available MCP tools
4. You should see: convert_file, convert_url, convert_batch, get_supported_formats
```

---

## 🔧 Troubleshooting

### Issue: VS Code doesn't see MCP tools

**Fix:**
1. Check config path: `~/.config/mcp/config.json` exists
2. Verify absolute paths in config.json
3. Restart VS Code completely (Cmd+Q)
4. Check VS Code Output panel → MCP

### Issue: "Command not found"

**Fix:**
```bash
# Make sure virtual environment exists
ls -la /Users/syedraza/mcp-local/.venv/bin/python

# If not, create it:
cd /Users/syedraza/mcp-local
python3 -m venv .venv
source .venv/bin/activate
pip install fastmcp markitdown
```

---

## 🎯 Summary

**Traditional MCP = STDIO Protocol**

- Used by: VS Code Copilot, Claude Desktop, MCP Inspector
- Protocol: JSON-RPC 2.0 over STDIN/STDOUT
- No web UI, no HTTP - pure MCP protocol
- Configuration: `~/.config/mcp/config.json`

**Your MCP server is ready at:**
- Command: `/Users/syedraza/mcp-local/.venv/bin/python`
- Script: `./markitdown_server/server.py`
- Tools: 4 (convert_file, convert_url, convert_batch, get_supported_formats)
