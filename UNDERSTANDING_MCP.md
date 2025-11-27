# Understanding MCP (Model Context Protocol)

## 🤔 What is MCP?

**MCP (Model Context Protocol)** is a **standardized protocol** that allows **AI assistants** (like Claude, GitHub Copilot, or custom AI agents) to **use tools and access data** from external services.

Think of it like this:
- **Without MCP**: AI can only chat with you using text
- **With MCP**: AI can perform real actions (convert files, query databases, search web, etc.)

---

## 🎯 Role of MCP in Your Project

Your project provides **document conversion tools** (PDF → Markdown, DOCX → Markdown, etc.) to AI assistants through MCP.

### Real-World Example:

**WITHOUT MCP (Traditional):**
```
You: "Convert my PDF to markdown"
AI: "I can't do that. Here's code you can run manually..."
You: [Copy code, run manually, paste results back]
```

**WITH MCP (Your Setup):**
```
You: "@workspace Convert my PDF to markdown"
AI: [Automatically calls your MCP server tool]
AI: "Here's the converted markdown content!"
```

**The AI can now DO things, not just SUGGEST things!**

---

## 🔧 How MCP Works in Your Setup

```
┌─────────────────┐
│  VS Code Editor │
│   (You type)    │
└────────┬────────┘
         │
         │ User asks: "@workspace Convert file.pdf"
         │
         ▼
┌─────────────────────┐
│  GitHub Copilot     │
│  (AI Assistant)     │
└────────┬────────────┘
         │
         │ "I need a tool to convert PDFs!"
         │
         ▼
┌─────────────────────┐        ┌──────────────────────┐
│  MCP Protocol       │◄──────►│  Your MCP Server     │
│  (Communication)    │        │  (server.py)         │
└─────────────────────┘        └──────────┬───────────┘
                                          │
                                          │ Uses MarkItDown
                                          │
                                          ▼
                               ┌──────────────────────┐
                               │  MarkItDown Library  │
                               │  (Actual conversion) │
                               └──────────────────────┘
```

### Step-by-Step Flow:

1. **You ask**: "@workspace Convert `/path/to/file.pdf` to markdown"

2. **Copilot thinks**: "User wants PDF conversion. Let me check available MCP tools..."

3. **MCP discovers tools**: 
   - Reads your `~/.config/mcp/config.json`
   - Connects to `server.py` via STDIO (standard input/output)
   - Gets list of 4 available tools:
     * `convert_file` - Convert local file to markdown
     * `convert_url` - Convert web page to markdown
     * `convert_batch` - Convert multiple files
     * `get_supported_formats` - List supported formats

4. **Copilot calls tool**: 
   ```json
   {
     "jsonrpc": "2.0",
     "method": "tools/call",
     "params": {
       "name": "convert_file",
       "arguments": {
         "path": "/path/to/file.pdf"
       }
     }
   }
   ```

5. **Your server processes**:
   - Receives JSON-RPC message via STDIN
   - Calls MarkItDown to convert PDF
   - Returns markdown result

6. **Copilot responds**: Shows you the converted markdown!

---

## 🔄 Two Transport Methods

Your project supports **2 ways** to use MCP:

### 1. **STDIO Transport** (Traditional MCP)
- **For**: AI assistants (VS Code Copilot, Claude Desktop)
- **Protocol**: JSON-RPC over STDIN/STDOUT
- **File**: `markitdown_server/server.py`
- **Config**: `~/.config/mcp/config.json`
- **Port**: None (uses pipes)

**How it works:**
```bash
# AI assistant starts your server as a subprocess
python server.py

# Then communicates via text pipes (STDIN/STDOUT)
# AI writes JSON → Your server reads from STDIN
# Your server writes JSON → AI reads from STDOUT
```

**Why this method?**
- ✅ Secure (no network exposure)
- ✅ Direct process communication
- ✅ Standard MCP protocol
- ✅ Works with all MCP-compatible AI assistants

---

### 2. **HTTP Transport** (Modern Alternative)
- **For**: Web applications, API integrations, remote access
- **Protocol**: HTTP REST API with optional SSE streaming
- **File**: `markitdown_server/http_streaming_server.py`
- **Config**: None needed (direct HTTP calls)
- **Port**: 8080

**How it works:**
```bash
# Start HTTP server
python http_streaming_server.py

# Anyone can call MCP tools via HTTP
curl -X POST http://localhost:8080/api/call/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/file.pdf"}'
```

**Why this method?**
- ✅ Remote access (network)
- ✅ Web UI included (drag-drop files)
- ✅ Real-time streaming progress (SSE)
- ✅ Easy integration with any language
- ❌ Not standard MCP (custom implementation)

---

## 🛠️ The 4 MCP Tools You Provide

When an AI connects to your MCP server, it discovers these tools:

### 1. `convert_file`
**What it does**: Convert a local file to markdown

**Example use by AI:**
```
You: "Convert my meeting-notes.docx to markdown"
AI: [Calls convert_file tool]
AI: "Here's your converted document..."
```

**Tool definition:**
```python
@app.tool()
def convert_file(path: str) -> str:
    """Convert a file to Markdown"""
    result = MarkItDown().convert(path)
    return result.text_content
```

---

### 2. `convert_url`
**What it does**: Convert a web page to markdown

**Example use by AI:**
```
You: "Summarize the content of https://example.com/article"
AI: [Calls convert_url tool to get clean text]
AI: "Here's a summary: ..."
```

**Tool definition:**
```python
@app.tool()
def convert_url(url: str) -> str:
    """Convert a URL to Markdown"""
    result = MarkItDown().convert(url)
    return result.text_content
```

---

### 3. `convert_batch`
**What it does**: Convert multiple files at once

**Example use by AI:**
```
You: "Convert all PDFs in my reports folder"
AI: [Calls convert_batch tool with list of files]
AI: "Converted 5 files successfully!"
```

**Tool definition:**
```python
@app.tool()
def convert_batch(paths: list[str]) -> dict:
    """Convert multiple files"""
    results = {}
    for path in paths:
        results[path] = MarkItDown().convert(path).text_content
    return results
```

---

### 4. `get_supported_formats`
**What it does**: List all supported file formats

**Example use by AI:**
```
You: "Can you convert Excel files?"
AI: [Calls get_supported_formats tool]
AI: "Yes! I support: PDF, DOCX, XLSX, PPTX, and more..."
```

**Tool definition:**
```python
@app.tool()
def get_supported_formats() -> list[str]:
    """Get list of supported formats"""
    return ["pdf", "docx", "xlsx", "pptx", "html", "txt", 
            "json", "xml", "jpg", "png", "gif", "wav"]
```

---

## 🆚 Comparison: With vs Without MCP

### Scenario: Convert 5 PDFs to Markdown

#### **WITHOUT MCP** (Manual)
1. ⏱️ Write Python script to use MarkItDown
2. ⏱️ Run script manually for each file
3. ⏱️ Copy/paste results
4. ⏱️ Format output
5. ⏱️ Repeat for each file
6. **Time**: 15-30 minutes

#### **WITH MCP** (Automated)
1. ✅ Ask AI: "@workspace Convert these 5 PDFs: file1.pdf, file2.pdf, ..."
2. ✅ AI calls `convert_batch` tool
3. ✅ Results appear instantly
4. **Time**: 10 seconds

---

## 🎓 Key Concepts

### 1. **MCP Server = Tool Provider**
Your `server.py` is an **MCP server** that **provides tools** to AI assistants.

Think of it as:
- A **toolbox** that AI can use
- A **plugin** for AI assistants
- An **API** specifically designed for AI agents

### 2. **Tools = Functions AI Can Call**
Each `@app.tool()` decorator creates a tool that:
- Has a **name** (e.g., "convert_file")
- Has **parameters** (e.g., "path")
- Has a **description** (AI reads this to understand what it does)
- Returns **results** (the converted markdown text)

### 3. **Protocol = Communication Language**
MCP uses **JSON-RPC 2.0** as the communication format:

**Request from AI:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "convert_file",
    "arguments": {
      "path": "/path/to/file.pdf"
    }
  }
}
```

**Response from your server:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "# Converted Markdown\n\nThis is the PDF content..."
}
```

### 4. **Transport = How Messages Travel**
- **STDIO**: Messages travel through text pipes (secure, local)
- **HTTP**: Messages travel over network (flexible, remote)

---

## 🔍 What Makes MCP Special?

### Before MCP:
Every AI assistant had **different ways** to integrate tools:
- ChatGPT: Custom plugins
- Claude: Different API
- Copilot: Different format
- **Problem**: You'd need to write 3+ different implementations!

### With MCP:
One **standard protocol** works with **all AI assistants**:
- ✅ Write your tools once
- ✅ Works with Copilot, Claude, and any MCP-compatible AI
- ✅ Easy to add new tools
- ✅ Easy for AI to discover what tools you have

---

## 🚀 Real Use Cases

### 1. **Document Processing Workflow**
```
You: "@workspace Process all invoices in /invoices folder"
AI: 
  1. Lists all PDF files using file system
  2. Calls convert_batch tool with all invoice paths
  3. Extracts invoice data from markdown
  4. Creates summary spreadsheet
  5. Shows you the results
```

### 2. **Research Assistant**
```
You: "@workspace Summarize these 10 research papers"
AI:
  1. Calls convert_batch with all paper PDFs
  2. Reads converted markdown
  3. Uses its LLM to generate summaries
  4. Creates comparison table
```

### 3. **Content Migration**
```
You: "@workspace Convert all Word docs to markdown for my blog"
AI:
  1. Finds all .docx files
  2. Calls convert_batch
  3. Formats for blog (adds frontmatter)
  4. Saves to blog directory
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR WORKSPACE                       │
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │         AI Assistant (GitHub Copilot)            │ │
│  │                                                  │ │
│  │  "User wants to convert PDF..."                 │ │
│  │  "Let me check available MCP tools..."          │ │
│  └───────────────────┬──────────────────────────────┘ │
│                      │                                 │
│                      │ MCP Protocol (JSON-RPC)         │
│                      │                                 │
│  ┌───────────────────▼──────────────────────────────┐ │
│  │         MCP Server (server.py)                   │ │
│  │                                                  │ │
│  │  Tools Available:                               │ │
│  │  • convert_file(path) → markdown                │ │
│  │  • convert_url(url) → markdown                  │ │
│  │  • convert_batch(paths) → results               │ │
│  │  • get_supported_formats() → list               │ │
│  └───────────────────┬──────────────────────────────┘ │
│                      │                                 │
│                      │ Python API                      │
│                      │                                 │
│  ┌───────────────────▼──────────────────────────────┐ │
│  │         MarkItDown Library                       │ │
│  │                                                  │ │
│  │  • PDF parsing                                  │ │
│  │  • DOCX parsing                                 │ │
│  │  • Image OCR                                    │ │
│  │  • HTML conversion                              │ │
│  └──────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ Summary: Why MCP Matters

| Without MCP | With MCP |
|------------|----------|
| AI can only chat | AI can take actions |
| Manual work | Automated workflows |
| Copy/paste results | Direct integration |
| Different setup per AI | One setup for all AIs |
| Static responses | Dynamic tool usage |

**MCP turns AI from a "conversational partner" into an "intelligent agent" that can actually DO things for you.**

---

## 🎯 Quick Answer to Your Question

**"What is the role of MCP over here?"**

MCP is the **bridge** that lets AI assistants (like GitHub Copilot in VS Code) **use your document conversion tools automatically**.

Instead of:
1. ❌ Asking AI for code
2. ❌ Running code manually  
3. ❌ Copying results back

You get:
1. ✅ Ask AI to convert document
2. ✅ AI calls your MCP server automatically
3. ✅ Results appear instantly

**MCP = AI can use your tools directly, without manual intervention.**

---

## 📚 Learn More

- **Official MCP Docs**: https://modelcontextprotocol.io
- **Your STDIO Testing Guide**: [TESTING_MCP.md](TESTING_MCP.md)
- **Your Local Setup Guide**: [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md)
- **FastMCP Framework**: https://gofastmcp.com
