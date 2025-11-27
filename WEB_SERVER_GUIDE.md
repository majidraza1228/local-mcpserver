# MarkItDown Web Server Guide

## Overview

The MarkItDown Web Server provides a beautiful browser-based interface for uploading and converting documents to Markdown. This is a **FastAPI HTTP server** (not MCP protocol).

> **Note:** This is NOT an MCP implementation. For MCP server, see [TESTING_MCP.md](TESTING_MCP.md)

---

## Features

✨ **Beautiful User Interface**
- Drag & drop file upload
- Real-time conversion status
- Download converted files instantly
- Responsive design with animations

📤 **File Upload**
- Browse files or drag & drop
- Support for 12+ file formats
- Visual file size and name display

📥 **Instant Download**
- One-click download of converted Markdown
- Files include metadata headers
- Clean, formatted output

🎨 **Modern Design**
- Gradient backgrounds
- Smooth animations
- Mobile-responsive layout

---

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/syedraza/mcp-local
source .venv/bin/activate
pip install fastapi uvicorn python-multipart markitdown
```

### 2. Start the Web Server

**Option A: Using startup script**
```bash
./markitdown_server/start_web.sh
```

**Option B: Direct execution**
```bash
cd /Users/syedraza/mcp-local
source .venv/bin/activate
python markitdown_server/web_server.py
```

### 3. Open in Browser

Navigate to: **http://localhost:8000**

---

## How to Use

### Step 1: Access the Interface
Open your web browser and go to http://localhost:8000

### Step 2: Upload a File
- **Drag & Drop:** Drag any supported file onto the upload area
- **Click to Browse:** Click the upload area to select a file

### Step 3: Convert
Click the "Convert to Markdown" button

### Step 4: Download
Click "Download Markdown" to save the converted file

---

## Supported File Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | `.pdf` | PDF documents |
| Word | `.docx` | Microsoft Word |
| Excel | `.xlsx` | Microsoft Excel spreadsheets |
| PowerPoint | `.pptx` | Microsoft PowerPoint presentations |
| HTML | `.html` | HTML files |
| Text | `.txt` | Plain text files |
| JSON | `.json` | JSON files |
| XML | `.xml` | XML files |
| JPEG | `.jpg`, `.jpeg` | JPEG images (with OCR) |
| PNG | `.png` | PNG images (with OCR) |
| GIF | `.gif` | GIF images |
| Audio | `.wav` | Audio files (with transcription) |

---

## REST API Endpoints

The web server also provides REST API endpoints:

### POST /convert
Upload and convert a file

**Request:**
```bash
curl -X POST http://localhost:8000/convert \
  -F "file=@/path/to/document.pdf"
```

**Response:**
```json
{
  "success": true,
  "filename": "document.md",
  "message": "File converted successfully"
}
```

### GET /download/{filename}
Download converted file

**Request:**
```bash
curl http://localhost:8000/download/document.md -o document.md
```

### GET /api/formats
List supported formats

**Request:**
```bash
curl http://localhost:8000/api/formats
```

**Response:**
```json
{
  "supported_extensions": [".pdf", ".docx", ...],
  "formats": [
    {"ext": ".pdf", "name": "PDF Documents"},
    ...
  ]
}
```

### GET /api/health
Health check endpoint

**Request:**
```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "MarkItDown Web Service",
  "version": "1.0.0"
}
```

---

## Configuration

### Change Port

Edit `markitdown_server/web_server.py`:

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port here
```

### Change Upload Directory

Edit the configuration at the top of `web_server.py`:

```python
UPLOAD_DIR = Path("/Users/syedraza/Documents/markitdown/uploads")
OUTPUT_DIR = Path("/Users/syedraza/Documents/markitdown/converted")
```

---

## Output Files

Converted Markdown files are saved with:

**Location:** `/Users/syedraza/Documents/markitdown/converted/`

**Format:**
```markdown
<!-- 
Original: document.pdf
Converted: 2024-11-26 20:30:15
Title: Document Title
-->

[Markdown content here]
```

---

## Architecture

```
┌─────────────────┐
│   Web Browser   │
│  (User uploads  │
│     files)      │
└────────┬────────┘
         │ HTTP POST /convert
         │
┌────────▼────────┐
│ FastAPI Server  │
│  - HTML UI      │
│  - REST API     │
│  - File Upload  │
└────────┬────────┘
         │
┌────────▼────────┐
│   MarkItDown    │
│    Library      │
│  (Conversion)   │
└────────┬────────┘
         │
┌────────▼────────┐
│  Output Files   │
│   (.md files)   │
└─────────────────┘
```

---

## Comparison with Other Modes

| Feature | Web Server | MCP Server | File Watcher |
|---------|-----------|------------|--------------|
| **Interface** | Browser UI | AI Assistant | Automated |
| **Protocol** | HTTP/REST | MCP/STDIO | File System |
| **User Type** | Humans | AI Tools | Background |
| **Upload Method** | Drag & Drop | Tool Call | Folder Drop |
| **Framework** | FastAPI | FastMCP | Watchdog |
| **Port** | 8000 | N/A | N/A |
| **Interactive** | Yes | Yes | No |

---

## Troubleshooting

### Server Won't Start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
source .venv/bin/activate
pip install fastapi uvicorn python-multipart
```

### Port Already in Use

**Error:** `OSError: [Errno 48] Address already in use`

**Solution:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in web_server.py
```

### Can't Access from Other Devices

The server binds to `0.0.0.0` which allows external access.

**Access from another device:**
```
http://YOUR_IP_ADDRESS:8000
```

Find your IP:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

### Upload Fails

**Check file size limits** - FastAPI has default limits. To increase:

```python
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/convert")
async def convert_file(file: UploadFile = File(..., max_length=100_000_000)):  # 100MB
    ...
```

### Conversion Errors

**Check logs** in the terminal where the server is running. Common issues:
- Corrupted files
- Unsupported file format
- Missing dependencies for specific formats (e.g., OCR for images)

---

## Development

### Adding Custom Endpoints

```python
@app.get("/api/stats")
async def get_stats():
    """Custom endpoint for statistics"""
    return {
        "total_conversions": 123,
        "formats_used": {"pdf": 50, "docx": 40}
    }
```

### Customizing the UI

The HTML is embedded in the `home()` function. Edit the HTML/CSS/JavaScript directly in `web_server.py`.

### Adding Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Security Considerations

⚠️ **This is a local development server** - not production-ready

**For production deployment:**

1. **Add Authentication:**
```python
from fastapi.security import HTTPBasic
security = HTTPBasic()
```

2. **Enable HTTPS:**
```bash
uvicorn web_server:app --ssl-keyfile key.pem --ssl-certfile cert.pem
```

3. **Add Rate Limiting:**
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
```

4. **Validate File Types:**
```python
ALLOWED_EXTENSIONS = {'.pdf', '.docx', ...}
if file.filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
    raise HTTPException(400, "Invalid file type")
```

5. **Scan for Malware** before processing uploads

---

## Performance

### Concurrent Uploads

FastAPI handles concurrent requests automatically with async/await.

### Large Files

For files > 100MB, consider:
- Streaming uploads
- Background tasks with Celery
- Progress indicators

### Caching

Add caching for frequently converted files:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def convert_cached(file_hash):
    # Convert and cache result
    pass
```

---

## Running in Production

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker markitdown_server.web_server:app
```

### Using Docker

```dockerfile
FROM python:3.14
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn python-multipart markitdown
CMD ["uvicorn", "markitdown_server.web_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using systemd

Create `/etc/systemd/system/markitdown-web.service`:

```ini
[Unit]
Description=MarkItDown Web Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/Users/syedraza/mcp-local
ExecStart=/Users/syedraza/mcp-local/.venv/bin/python markitdown_server/web_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Related Documentation

- **[MCP Implementation](TESTING_MCP.md)** - Test the MCP server with AI assistants
- **[MCP vs Non-MCP Guide](MCP_IMPLEMENTATION_GUIDE.md)** - Understanding the differences
- **[File Watcher Service](README.md#c-file-watcher-service-mode)** - Automated conversion
- **[Main README](README.md)** - Project overview

---

## Support

**Issues?**
- Check the terminal output for error messages
- Verify dependencies are installed
- Ensure port 8000 is available
- Review [Troubleshooting](#troubleshooting) section

**Questions?**
- Open an issue on GitHub
- Check existing documentation
- Review FastAPI docs: https://fastapi.tiangolo.com
