#!/usr/bin/env python3
"""
MarkItDown FastAPI Web Server

Web interface for uploading and converting documents to Markdown.
Provides both a browser UI and REST API endpoints.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from markitdown import MarkItDown
import os
import shutil
from pathlib import Path
from datetime import datetime
import tempfile
import uvicorn

# Configuration
UPLOAD_DIR = Path("/Users/syedraza/Documents/markitdown/uploads")
OUTPUT_DIR = Path("/Users/syedraza/Documents/markitdown/converted")

# Create directories
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize FastAPI and MarkItDown
app = FastAPI(
    title="MarkItDown Web Service",
    description="Upload documents and convert them to Markdown",
    version="1.0.0"
)

md = MarkItDown()

# Supported extensions
SUPPORTED_EXTENSIONS = {
    '.pdf', '.docx', '.xlsx', '.pptx',
    '.html', '.txt', '.json', '.xml',
    '.jpg', '.jpeg', '.png', '.gif', '.wav'
}

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main upload page."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MarkItDown Converter</title>
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
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 800px;
                width: 100%;
                padding: 40px;
            }
            
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 2.5em;
                text-align: center;
            }
            
            .subtitle {
                color: #666;
                text-align: center;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            
            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 15px;
                padding: 60px 20px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                background: #f8f9ff;
                margin-bottom: 30px;
            }
            
            .upload-area:hover {
                border-color: #764ba2;
                background: #f0f2ff;
            }
            
            .upload-area.dragover {
                border-color: #764ba2;
                background: #e8ebff;
                transform: scale(1.02);
            }
            
            .upload-icon {
                font-size: 4em;
                margin-bottom: 20px;
            }
            
            .upload-text {
                font-size: 1.2em;
                color: #667eea;
                margin-bottom: 10px;
                font-weight: 600;
            }
            
            .upload-hint {
                color: #999;
                font-size: 0.9em;
            }
            
            input[type="file"] {
                display: none;
            }
            
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 40px;
                border: none;
                border-radius: 10px;
                font-size: 1.1em;
                cursor: pointer;
                transition: transform 0.2s;
                width: 100%;
                font-weight: 600;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }
            
            .file-info {
                background: #f8f9ff;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                display: none;
            }
            
            .file-name {
                font-weight: 600;
                color: #333;
                margin-bottom: 5px;
            }
            
            .file-size {
                color: #666;
                font-size: 0.9em;
            }
            
            .status {
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                display: none;
                animation: fadeIn 0.3s;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .status.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .status.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .status.processing {
                background: #d1ecf1;
                color: #0c5460;
                border: 1px solid #bee5eb;
            }
            
            .download-btn {
                display: inline-block;
                margin-top: 10px;
                padding: 10px 20px;
                background: #28a745;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: 600;
            }
            
            .download-btn:hover {
                background: #218838;
            }
            
            .formats {
                margin-top: 30px;
                padding-top: 30px;
                border-top: 1px solid #eee;
            }
            
            .formats-title {
                font-weight: 600;
                color: #333;
                margin-bottom: 15px;
            }
            
            .format-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            
            .format-tag {
                background: #e8ebff;
                color: #667eea;
                padding: 8px 15px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: 600;
            }
            
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                display: inline-block;
                margin-right: 10px;
                vertical-align: middle;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 MarkItDown</h1>
            <p class="subtitle">Convert documents to Markdown instantly</p>
            
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📎</div>
                <div class="upload-text">Drop your file here or click to browse</div>
                <div class="upload-hint">PDF, DOCX, XLSX, PPTX, Images, Audio & more</div>
                <input type="file" id="fileInput" accept=".pdf,.docx,.xlsx,.pptx,.html,.txt,.json,.xml,.jpg,.jpeg,.png,.gif,.wav">
            </div>
            
            <div class="file-info" id="fileInfo">
                <div class="file-name" id="fileName"></div>
                <div class="file-size" id="fileSize"></div>
            </div>
            
            <button class="btn" id="convertBtn" onclick="convertFile()" disabled>
                Convert to Markdown
            </button>
            
            <div class="status" id="status"></div>
            
            <div class="formats">
                <div class="formats-title">✨ Supported Formats</div>
                <div class="format-tags">
                    <span class="format-tag">PDF</span>
                    <span class="format-tag">DOCX</span>
                    <span class="format-tag">XLSX</span>
                    <span class="format-tag">PPTX</span>
                    <span class="format-tag">HTML</span>
                    <span class="format-tag">TXT</span>
                    <span class="format-tag">JSON</span>
                    <span class="format-tag">XML</span>
                    <span class="format-tag">JPG/PNG</span>
                    <span class="format-tag">GIF</span>
                    <span class="format-tag">WAV</span>
                </div>
            </div>
        </div>
        
        <script>
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const fileInfo = document.getElementById('fileInfo');
            const fileName = document.getElementById('fileName');
            const fileSize = document.getElementById('fileSize');
            const convertBtn = document.getElementById('convertBtn');
            const status = document.getElementById('status');
            
            let selectedFile = null;
            
            // Click to upload
            uploadArea.addEventListener('click', () => fileInput.click());
            
            // Drag and drop
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFile(files[0]);
                }
            });
            
            // File input change
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFile(e.target.files[0]);
                }
            });
            
            function handleFile(file) {
                selectedFile = file;
                fileName.textContent = `📄 ${file.name}`;
                fileSize.textContent = `Size: ${formatBytes(file.size)}`;
                fileInfo.style.display = 'block';
                convertBtn.disabled = false;
                status.style.display = 'none';
            }
            
            function formatBytes(bytes) {
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
            }
            
            async function convertFile() {
                if (!selectedFile) return;
                
                const formData = new FormData();
                formData.append('file', selectedFile);
                
                // Show processing status
                status.className = 'status processing';
                status.style.display = 'block';
                status.innerHTML = '<div class="spinner"></div>Converting your document...';
                convertBtn.disabled = true;
                
                try {
                    const response = await fetch('/convert', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        status.className = 'status success';
                        status.innerHTML = `
                            ✅ Conversion successful!
                            <br>
                            <a href="/download/${result.filename}" class="download-btn" download>
                                ⬇️ Download Markdown
                            </a>
                        `;
                    } else {
                        throw new Error(result.detail || 'Conversion failed');
                    }
                } catch (error) {
                    status.className = 'status error';
                    status.innerHTML = `❌ Error: ${error.message}`;
                } finally {
                    convertBtn.disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    """Convert uploaded file to Markdown."""
    
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    
    # Save uploaded file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_ext)
    try:
        # Write uploaded content to temp file
        content = await file.read()
        temp_file.write(content)
        temp_file.close()
        
        # Convert to markdown
        result = md.convert(temp_file.name)
        
        # Generate output filename
        output_filename = Path(file.filename).stem + ".md"
        output_path = OUTPUT_DIR / output_filename
        
        # Handle duplicate filenames
        counter = 1
        while output_path.exists():
            output_filename = f"{Path(file.filename).stem}_{counter}.md"
            output_path = OUTPUT_DIR / output_filename
            counter += 1
        
        # Write markdown content
        with open(output_path, 'w', encoding='utf-8') as f:
            # Add metadata header
            f.write(f"<!-- \n")
            f.write(f"Original: {file.filename}\n")
            f.write(f"Converted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            if hasattr(result, 'title') and result.title:
                f.write(f"Title: {result.title}\n")
            f.write(f"-->\n\n")
            
            # Write content
            f.write(result.text_content)
        
        return JSONResponse({
            "success": True,
            "filename": output_filename,
            "message": "File converted successfully"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up temp file
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download converted markdown file."""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/markdown"
    )

@app.get("/api/formats")
async def get_formats():
    """Get list of supported formats."""
    return {
        "supported_extensions": list(SUPPORTED_EXTENSIONS),
        "formats": [
            {"ext": ".pdf", "name": "PDF Documents"},
            {"ext": ".docx", "name": "Microsoft Word"},
            {"ext": ".xlsx", "name": "Microsoft Excel"},
            {"ext": ".pptx", "name": "Microsoft PowerPoint"},
            {"ext": ".html", "name": "HTML Files"},
            {"ext": ".txt", "name": "Text Files"},
            {"ext": ".json", "name": "JSON Files"},
            {"ext": ".xml", "name": "XML Files"},
            {"ext": ".jpg/.jpeg", "name": "JPEG Images (OCR)"},
            {"ext": ".png", "name": "PNG Images (OCR)"},
            {"ext": ".gif", "name": "GIF Images"},
            {"ext": ".wav", "name": "Audio Files (Transcription)"}
        ]
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "MarkItDown Web Service",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    print("=" * 60)
    print("MarkItDown Web Service")
    print("=" * 60)
    print(f"📁 Uploads: {UPLOAD_DIR}")
    print(f"📄 Output: {OUTPUT_DIR}")
    print(f"🌐 Starting web server on http://localhost:8000")
    print("=" * 60)
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
