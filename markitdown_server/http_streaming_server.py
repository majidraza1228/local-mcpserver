#!/usr/bin/env python3
"""
MarkItDown Unified HTTP Server
Single server with MCP tools API, Web UI, and streaming support.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from markitdown import MarkItDown
import uvicorn
import json
import asyncio
from pathlib import Path
import tempfile
import os
from datetime import datetime

# Initialize FastMCP
mcp = FastMCP(name="markitdown")

markitdown = MarkItDown()

SUPPORTED_FORMATS = [
    "pdf", "docx", "xlsx", "pptx", "html", "txt",
    "json", "xml", "jpg", "jpeg", "png", "gif", "wav"
]

# MCP Tools
@mcp.tool()
def convert_file(path: str) -> str:
    """Convert a local file to Markdown format."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    result = markitdown.convert(path)
    return result.text_content

@mcp.tool()
def convert_url(url: str) -> str:
    """Convert a web page to Markdown format."""
    result = markitdown.convert(url)
    return result.text_content

@mcp.tool()
def convert_batch(paths: list[str]) -> dict:
    """Convert multiple files to Markdown format."""
    results = {}
    for path in paths:
        try:
            if os.path.exists(path):
                result = markitdown.convert(path)
                results[path] = result.text_content
            else:
                results[path] = f"Error: File not found"
        except Exception as e:
            results[path] = f"Error: {str(e)}"
    return results

@mcp.tool()
def get_supported_formats() -> list[str]:
    """Get list of supported file formats."""
    return SUPPORTED_FORMATS

# FastAPI app
app = FastAPI(
    title="MarkItDown HTTP Streaming Server",
    description="Unified server with MCP tools, Web UI, and SSE streaming",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Streaming helper
async def stream_conversion(file_path: str, filename: str):
    """Stream conversion progress and result"""
    try:
        yield f"data: {json.dumps({'type': 'start', 'filename': filename, 'timestamp': datetime.now().isoformat()})}\n\n"
        await asyncio.sleep(0.1)
        
        yield f"data: {json.dumps({'type': 'progress', 'message': 'Reading file...', 'percent': 30})}\n\n"
        await asyncio.sleep(0.1)
        
        yield f"data: {json.dumps({'type': 'progress', 'message': 'Converting to Markdown...', 'percent': 60})}\n\n"
        await asyncio.sleep(0.1)
        
        result = markitdown.convert(file_path)
        
        yield f"data: {json.dumps({'type': 'progress', 'message': 'Finalizing...', 'percent': 90})}\n\n"
        await asyncio.sleep(0.1)
        
        yield f"data: {json.dumps({'type': 'complete', 'content': result.text_content, 'percent': 100})}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    finally:
        if os.path.exists(file_path):
            os.unlink(file_path)

async def stream_tool_execution(tool_name: str, args: dict):
    """Stream MCP tool execution"""
    try:
        yield f"data: {json.dumps({'type': 'start', 'tool': tool_name, 'timestamp': datetime.now().isoformat()})}\n\n"
        await asyncio.sleep(0.1)
        
        yield f"data: {json.dumps({'type': 'progress', 'message': f'Executing {tool_name}...', 'percent': 50})}\n\n"
        await asyncio.sleep(0.1)
        
        if tool_name == "convert_file":
            result = convert_file(args.get("path"))
        elif tool_name == "convert_url":
            result = convert_url(args.get("url"))
        elif tool_name == "convert_batch":
            result = convert_batch(args.get("paths"))
        elif tool_name == "get_supported_formats":
            result = get_supported_formats()
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        yield f"data: {json.dumps({'type': 'complete', 'result': result, 'percent': 100})}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

@app.get("/", response_class=HTMLResponse)
async def root():
    """Web UI with streaming"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarkItDown HTTP Streaming Server</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.1em; }
        .tabs {
            display: flex;
            background: #f8f9ff;
            border-bottom: 2px solid #667eea;
        }
        .tab {
            flex: 1;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 1.1em;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
        }
        .tab.active {
            background: white;
            color: #667eea;
            border-bottom: 3px solid #667eea;
        }
        .tab:hover { background: #f0f1ff; }
        .tab-content { display: none; padding: 40px; }
        .tab-content.active { display: block; }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 60px 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #f8f9ff;
        }
        .upload-area:hover {
            border-color: #764ba2;
            background: #f0f1ff;
            transform: scale(1.02);
        }
        .upload-area.dragging {
            background: #e8e9ff;
            border-color: #764ba2;
            transform: scale(1.05);
        }
        .upload-icon { font-size: 4em; margin-bottom: 20px; }
        .upload-text {
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 10px;
            font-weight: 600;
        }
        .upload-hint { color: #666; font-size: 0.95em; }
        .progress-container { display: none; margin-top: 30px; }
        .progress-bar-container {
            background: #e0e0e0;
            border-radius: 10px;
            height: 30px;
            overflow: hidden;
            margin-bottom: 15px;
        }
        .progress-bar {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            width: 0%;
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        .progress-message {
            text-align: center;
            color: #667eea;
            font-size: 1.1em;
            font-weight: 500;
        }
        .result-container { display: none; margin-top: 30px; }
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .result-title {
            font-size: 1.3em;
            color: #667eea;
            font-weight: 600;
        }
        .result-content {
            background: #f8f9ff;
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 0.9em;
            line-height: 1.6;
        }
        .button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: transform 0.2s;
        }
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .api-section {
            background: #f8f9ff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .api-section h3 {
            color: #667eea;
            margin-bottom: 15px;
        }
        .endpoint {
            background: white;
            border: 2px solid #667eea;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .endpoint-method {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.9em;
            margin-right: 10px;
        }
        .endpoint-path {
            font-family: 'Courier New', monospace;
            color: #764ba2;
            font-weight: 600;
        }
        .endpoint-desc {
            margin-top: 10px;
            color: #666;
        }
        code {
            background: #f0f1ff;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #667eea;
        }
        input[type="file"] { display: none; }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-indicator.processing {
            background: #ffa500;
            animation: pulse 1.5s ease-in-out infinite;
        }
        .status-indicator.complete { background: #4caf50; }
        .status-indicator.error { background: #f44336; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 MarkItDown HTTP Streaming</h1>
            <p>MCP Tools API + Web UI + Real-time Streaming</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('upload')">📤 Upload & Convert</button>
            <button class="tab" onclick="showTab('api')">📡 API Reference</button>
        </div>
        
        <div id="upload-tab" class="tab-content active">
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📤</div>
                <div class="upload-text">Drop file here or click to upload</div>
                <div class="upload-hint">PDF, DOCX, XLSX, PPTX, Images & more</div>
                <input type="file" id="fileInput" accept="*/*">
            </div>
            
            <div class="progress-container" id="progressContainer">
                <div class="progress-bar-container">
                    <div class="progress-bar" id="progressBar">0%</div>
                </div>
                <div class="progress-message" id="progressMessage">
                    <span class="status-indicator processing"></span>
                    <span id="statusText">Starting conversion...</span>
                </div>
            </div>
            
            <div class="result-container" id="resultContainer">
                <div class="result-header">
                    <div class="result-title">
                        <span class="status-indicator complete"></span>
                        Conversion Complete
                    </div>
                    <button class="button" onclick="downloadMarkdown()">Download</button>
                </div>
                <div class="result-content" id="resultContent"></div>
            </div>
        </div>
        
        <div id="api-tab" class="tab-content">
            <div class="api-section">
                <h3>🔧 MCP Tools API</h3>
                
                <div class="endpoint">
                    <span class="endpoint-method">GET</span>
                    <span class="endpoint-path">/api/tools</span>
                    <div class="endpoint-desc">List all available MCP tools</div>
                </div>
                
                <div class="endpoint">
                    <span class="endpoint-method">POST</span>
                    <span class="endpoint-path">/api/stream/convert</span>
                    <div class="endpoint-desc">
                        Upload and convert file with streaming progress (SSE)<br>
                        <code>Content-Type: multipart/form-data</code>
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="endpoint-method">POST</span>
                    <span class="endpoint-path">/api/call/convert_file</span>
                    <div class="endpoint-desc">
                        Convert local file: <code>{"path": "/absolute/path/to/file.pdf"}</code>
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="endpoint-method">POST</span>
                    <span class="endpoint-path">/api/call/convert_url</span>
                    <div class="endpoint-desc">
                        Convert web page: <code>{"url": "https://example.com"}</code>
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="endpoint-method">POST</span>
                    <span class="endpoint-path">/api/call/convert_batch</span>
                    <div class="endpoint-desc">
                        Convert multiple files: <code>{"paths": ["/path/1.pdf", "/path/2.docx"]}</code>
                    </div>
                </div>
                
                <div class="endpoint">
                    <span class="endpoint-method">GET</span>
                    <span class="endpoint-path">/api/formats</span>
                    <div class="endpoint-desc">Get list of supported file formats</div>
                </div>
            </div>
            
            <div class="api-section">
                <h3>📋 Example Usage</h3>
                <div style="background: white; padding: 15px; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 0.9em;">
# Upload with streaming<br>
curl -N -X POST http://localhost:8080/api/stream/convert \\<br>
  -F "file=@document.pdf"<br>
<br>
# Call MCP tool<br>
curl -X POST http://localhost:8080/api/call/convert_file \\<br>
  -H "Content-Type: application/json" \\<br>
  -d '{"path": "/path/to/file.pdf"}'<br>
<br>
# Get formats<br>
curl http://localhost:8080/api/formats
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let convertedContent = '';
        let currentFilename = '';
        
        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabName + '-tab').classList.add('active');
        }
        
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const progressContainer = document.getElementById('progressContainer');
        const progressBar = document.getElementById('progressBar');
        const statusText = document.getElementById('statusText');
        const resultContainer = document.getElementById('resultContainer');
        const resultContent = document.getElementById('resultContent');
        
        uploadArea.onclick = () => fileInput.click();
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragging');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragging');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragging');
            const file = e.dataTransfer.files[0];
            if (file) handleFile(file);
        });
        
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) handleFile(file);
        });
        
        async function handleFile(file) {
            currentFilename = file.name;
            uploadArea.style.display = 'none';
            progressContainer.style.display = 'block';
            resultContainer.style.display = 'none';
            
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await fetch('/api/stream/convert', {
                    method: 'POST',
                    body: formData
                });
                
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    
                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\\n\\n');
                    
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = JSON.parse(line.slice(6));
                            handleStreamEvent(data);
                        }
                    }
                }
            } catch (error) {
                showError(error.message);
            }
        }
        
        function handleStreamEvent(data) {
            switch (data.type) {
                case 'start':
                    statusText.textContent = `Converting ${data.filename}...`;
                    break;
                case 'progress':
                    progressBar.style.width = `${data.percent}%`;
                    progressBar.textContent = `${data.percent}%`;
                    statusText.textContent = data.message;
                    break;
                case 'complete':
                    progressBar.style.width = '100%';
                    progressBar.textContent = '100%';
                    convertedContent = data.content;
                    showResult(data.content);
                    break;
                case 'error':
                    showError(data.message);
                    break;
            }
        }
        
        function showResult(content) {
            setTimeout(() => {
                progressContainer.style.display = 'none';
                resultContainer.style.display = 'block';
                resultContent.textContent = content;
                uploadArea.style.display = 'block';
            }, 500);
        }
        
        function showError(message) {
            statusText.innerHTML = `<span class="status-indicator error"></span>Error: ${message}`;
            setTimeout(() => {
                uploadArea.style.display = 'block';
                progressContainer.style.display = 'none';
            }, 3000);
        }
        
        function downloadMarkdown() {
            const blob = new Blob([convertedContent], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = currentFilename.replace(/\\.[^/.]+$/, '') + '.md';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    </script>
</body>
</html>
    """

@app.get("/api/tools")
async def list_tools():
    """List all MCP tools"""
    return {
        "tools": [
            {"name": "convert_file", "description": "Convert a local file to Markdown"},
            {"name": "convert_url", "description": "Convert a web page to Markdown"},
            {"name": "convert_batch", "description": "Convert multiple files to Markdown"},
            {"name": "get_supported_formats", "description": "Get supported file formats"}
        ]
    }

@app.get("/api/formats")
async def get_formats():
    """Get supported formats"""
    return {"formats": SUPPORTED_FORMATS}

@app.post("/api/call/{tool_name}")
async def call_tool(tool_name: str, args: dict):
    """Call MCP tool (JSON response)"""
    try:
        if tool_name == "convert_file":
            result = convert_file(args.get("path"))
        elif tool_name == "convert_url":
            result = convert_url(args.get("url"))
        elif tool_name == "convert_batch":
            result = convert_batch(args.get("paths"))
        elif tool_name == "get_supported_formats":
            result = get_supported_formats()
        else:
            raise HTTPException(status_code=404, detail=f"Tool not found: {tool_name}")
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stream/{tool_name}")
async def stream_tool(tool_name: str, args: dict):
    """Call MCP tool with streaming (SSE)"""
    return StreamingResponse(
        stream_tool_execution(tool_name, args),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )

@app.post("/api/stream/convert")
async def convert_upload(file: UploadFile = File(...)):
    """Upload and convert with streaming"""
    suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    return StreamingResponse(
        stream_conversion(tmp_path, file.filename),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "streaming": "enabled", "mcp_tools": 4}

if __name__ == "__main__":
    print("🚀 Starting MarkItDown HTTP Streaming Server...")
    print("📡 MCP Tools + Web UI + SSE Streaming - All in One")
    print("🌐 Server: http://localhost:8080")
    print("\n✨ Features:")
    print("   • Web UI for file uploads")
    print("   • MCP tools accessible via HTTP API")
    print("   • Real-time streaming progress (SSE)")
    print("   • 4 MCP tools: convert_file, convert_url, convert_batch, get_supported_formats")
    print("\nPress Ctrl+C to stop")
    
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
