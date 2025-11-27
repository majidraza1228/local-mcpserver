#!/usr/bin/env python3
"""
MarkItDown Streaming HTTP Server
Provides real-time streaming responses for document conversion with progress updates.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from markitdown import MarkItDown
import json
import asyncio
from pathlib import Path
import tempfile
import os
from datetime import datetime

app = FastAPI(
    title="MarkItDown Streaming Server",
    description="Convert documents to Markdown with real-time streaming progress",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

markitdown = MarkItDown()

# Supported formats
SUPPORTED_FORMATS = {
    "pdf": "PDF Documents",
    "docx": "Word Documents",
    "xlsx": "Excel Spreadsheets",
    "pptx": "PowerPoint Presentations",
    "html": "HTML Files",
    "txt": "Text Files",
    "json": "JSON Files",
    "xml": "XML Files",
    "jpg": "JPEG Images",
    "jpeg": "JPEG Images",
    "png": "PNG Images",
    "gif": "GIF Images",
    "wav": "WAV Audio Files"
}


async def stream_conversion(file_path: str, filename: str):
    """Stream conversion progress and result as Server-Sent Events"""
    try:
        # Send start event
        yield f"data: {json.dumps({'type': 'start', 'filename': filename, 'timestamp': datetime.now().isoformat()})}\n\n"
        await asyncio.sleep(0.1)
        
        # Send progress event
        yield f"data: {json.dumps({'type': 'progress', 'message': 'Reading file...', 'percent': 30})}\n\n"
        await asyncio.sleep(0.1)
        
        # Convert the file
        yield f"data: {json.dumps({'type': 'progress', 'message': 'Converting to Markdown...', 'percent': 60})}\n\n"
        await asyncio.sleep(0.1)
        
        result = markitdown.convert(file_path)
        
        yield f"data: {json.dumps({'type': 'progress', 'message': 'Finalizing...', 'percent': 90})}\n\n"
        await asyncio.sleep(0.1)
        
        # Send completion event
        yield f"data: {json.dumps({'type': 'complete', 'content': result.text_content, 'percent': 100})}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    finally:
        # Clean up temp file
        if os.path.exists(file_path):
            os.unlink(file_path)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Streaming UI with real-time progress"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarkItDown Streaming Server</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .content {
            padding: 40px;
        }
        
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 60px 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
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
        
        .upload-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        .upload-text {
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        .upload-hint {
            color: #666;
            font-size: 0.95em;
        }
        
        .progress-container {
            display: none;
            margin-top: 30px;
        }
        
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
            transition: width 0.3s ease;
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
        
        .result-container {
            display: none;
            margin-top: 30px;
        }
        
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
            transition: transform 0.2s ease;
        }
        
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .button:active {
            transform: translateY(0);
        }
        
        .formats {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9ff;
            border-radius: 10px;
        }
        
        .formats h3 {
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .format-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }
        
        .format-tag {
            background: white;
            border: 2px solid #667eea;
            padding: 8px 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
            color: #667eea;
        }
        
        input[type="file"] {
            display: none;
        }
        
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
        
        .status-indicator.complete {
            background: #4caf50;
        }
        
        .status-indicator.error {
            background: #f44336;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 MarkItDown Streaming</h1>
            <p>Real-time document conversion with progress tracking</p>
        </div>
        
        <div class="content">
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
            
            <div class="formats">
                <h3>✨ Supported Formats</h3>
                <div class="format-grid">
                    <div class="format-tag">PDF</div>
                    <div class="format-tag">DOCX</div>
                    <div class="format-tag">XLSX</div>
                    <div class="format-tag">PPTX</div>
                    <div class="format-tag">HTML</div>
                    <div class="format-tag">TXT</div>
                    <div class="format-tag">JSON</div>
                    <div class="format-tag">XML</div>
                    <div class="format-tag">JPG/PNG</div>
                    <div class="format-tag">WAV</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const progressContainer = document.getElementById('progressContainer');
        const progressBar = document.getElementById('progressBar');
        const progressMessage = document.getElementById('progressMessage');
        const statusText = document.getElementById('statusText');
        const resultContainer = document.getElementById('resultContainer');
        const resultContent = document.getElementById('resultContent');
        let convertedContent = '';
        let currentFilename = '';
        
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
                const response = await fetch('/convert/stream', {
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
            a.download = currentFilename.replace(/\.[^/.]+$/, '') + '.md';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    </script>
</body>
</html>
    """


@app.post("/convert/stream")
async def convert_file_stream(file: UploadFile = File(...)):
    """Convert file with streaming progress updates"""
    
    # Save uploaded file temporarily
    suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    # Stream the conversion
    return StreamingResponse(
        stream_conversion(tmp_path, file.filename),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/api/formats")
async def get_formats():
    """Get supported file formats"""
    return {"formats": SUPPORTED_FORMATS}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "markitdown-streaming"}


if __name__ == "__main__":
    print("🚀 Starting MarkItDown Streaming Server...")
    print("📡 Server will run on: http://localhost:8001")
    print("🔄 Real-time streaming enabled")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
