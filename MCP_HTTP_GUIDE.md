# MCP HTTP Server Guide

Complete guide for using the MarkItDown MCP server over HTTP with streaming support.

---

## 🎯 Overview

The MCP HTTP server exposes all MCP tools via HTTP REST API with Server-Sent Events (SSE) for real-time streaming progress updates.

**Key Features:**
- ✅ RESTful API for all MCP tools
- ✅ Server-Sent Events (SSE) for streaming responses
- ✅ File upload with progress tracking
- ✅ No STDIO transport needed - pure HTTP
- ✅ Easy integration with any HTTP client

---

## 🚀 Quick Start

### Start the Server

```bash
cd /Users/syedraza/mcp-local
.venv/bin/python markitdown_server/mcp_http_server.py
```

**Or use the launcher:**
```bash
./markitdown_server/start_mcp_http.sh
```

**Server runs on:** http://localhost:8002

---

## 📡 API Endpoints

### 1. Get Server Info
```bash
GET /
```

**Response:**
```json
{
  "service": "MarkItDown MCP HTTP Server",
  "version": "1.0.0",
  "transport": "HTTP with SSE streaming",
  "endpoints": {...}
}
```

### 2. List Available MCP Tools
```bash
GET /mcp/tools
```

**Response:**
```json
{
  "tools": [
    {
      "name": "convert_file",
      "description": "Convert a local file to Markdown",
      "parameters": {"path": "string (absolute file path)"}
    },
    {
      "name": "convert_url",
      "description": "Convert a web page to Markdown",
      "parameters": {"url": "string (web URL)"}
    },
    {
      "name": "convert_batch",
      "description": "Convert multiple files to Markdown",
      "parameters": {"paths": "array of strings (file paths)"}
    },
    {
      "name": "get_supported_formats",
      "description": "Get list of supported file formats",
      "parameters": {}
    }
  ]
}
```

### 3. Call MCP Tool (JSON Response)
```bash
POST /mcp/call/{tool_name}
Content-Type: application/json
```

**Examples:**

**Convert a file:**
```bash
curl -X POST http://localhost:8002/mcp/call/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/Users/syedraza/Documents/test.pdf"}'
```

**Convert a URL:**
```bash
curl -X POST http://localhost:8002/mcp/call/convert_url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Batch conversion:**
```bash
curl -X POST http://localhost:8002/mcp/call/convert_batch \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/path/to/file1.pdf", "/path/to/file2.docx"]}'
```

**Get supported formats:**
```bash
curl -X POST http://localhost:8002/mcp/call/get_supported_formats \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response:**
```json
{
  "success": true,
  "result": "...markdown content..."
}
```

### 4. Call MCP Tool with Streaming (SSE)
```bash
POST /mcp/stream/{tool_name}
Content-Type: application/json
```

**Example:**
```bash
curl -N -X POST http://localhost:8002/mcp/stream/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/Users/syedraza/Documents/test.pdf"}'
```

**Response (Server-Sent Events):**
```
data: {"type": "start", "tool": "convert_file", "timestamp": "2025-11-26T..."}

data: {"type": "progress", "message": "Executing convert_file...", "percent": 30}

data: {"type": "progress", "message": "Finalizing...", "percent": 90}

data: {"type": "complete", "result": "...markdown...", "percent": 100}
```

### 5. Upload File and Convert (Streaming)
```bash
POST /mcp/upload
Content-Type: multipart/form-data
```

**Example:**
```bash
curl -N -X POST http://localhost:8002/mcp/upload \
  -F "file=@/Users/syedraza/Documents/test.pdf"
```

**Response (SSE):**
```
data: {"type": "start", "filename": "test.pdf"}

data: {"type": "progress", "message": "Processing upload...", "percent": 30}

data: {"type": "progress", "message": "Finalizing...", "percent": 90}

data: {"type": "complete", "result": "...markdown...", "percent": 100}
```

---

## 💻 Using from Code

### Python Example

```python
import requests
import json

# Non-streaming request
response = requests.post(
    "http://localhost:8002/mcp/call/convert_file",
    json={"path": "/path/to/file.pdf"}
)
result = response.json()
print(result["result"])

# Streaming request (SSE)
response = requests.post(
    "http://localhost:8002/mcp/stream/convert_file",
    json={"path": "/path/to/file.pdf"},
    stream=True
)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = json.loads(line[6:])
            print(f"{data['type']}: {data.get('message', data.get('percent', ''))}")

# Upload file with streaming
with open("/path/to/file.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8002/mcp/upload",
        files={"file": f},
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = json.loads(line[6:])
                print(f"{data['type']}: {data.get('message', '')}")
```

### JavaScript Example

```javascript
// Non-streaming request
async function convertFile(path) {
  const response = await fetch('http://localhost:8002/mcp/call/convert_file', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path })
  });
  const data = await response.json();
  return data.result;
}

// Streaming request (SSE)
function convertFileStreaming(path) {
  fetch('http://localhost:8002/mcp/stream/convert_file', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path })
  }).then(response => {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    function read() {
      reader.read().then(({ done, value }) => {
        if (done) return;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n\n');
        
        lines.forEach(line => {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));
            console.log(`${data.type}: ${data.message || data.percent || ''}`);
            
            if (data.type === 'complete') {
              console.log('Result:', data.result);
            }
          }
        });
        
        read();
      });
    }
    
    read();
  });
}

// Upload file with streaming
async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8002/mcp/upload', {
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
        console.log(`${data.type}: ${data.message || data.percent || ''}`);
      }
    }
  }
}

// Usage
convertFile('/path/to/file.pdf');
convertFileStreaming('/path/to/file.pdf');
```

### cURL Examples

```bash
# Get server info
curl http://localhost:8002/

# List tools
curl http://localhost:8002/mcp/tools

# Convert file (JSON)
curl -X POST http://localhost:8002/mcp/call/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/Users/syedraza/Documents/test.pdf"}'

# Convert file (Streaming)
curl -N -X POST http://localhost:8002/mcp/stream/convert_file \
  -H "Content-Type: application/json" \
  -d '{"path": "/Users/syedraza/Documents/test.pdf"}'

# Convert URL
curl -X POST http://localhost:8002/mcp/call/convert_url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Batch convert
curl -X POST http://localhost:8002/mcp/call/convert_batch \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/path/1.pdf", "/path/2.docx"]}'

# Upload file
curl -N -X POST http://localhost:8002/mcp/upload \
  -F "file=@/Users/syedraza/Documents/test.pdf"

# Health check
curl http://localhost:8002/health
```

---

## 🔄 Streaming vs Non-Streaming

### Non-Streaming (`/mcp/call/{tool}`)
- **Use when:** You want a simple request/response
- **Response:** Single JSON response with complete result
- **Best for:** Scripts, simple integrations, batch processing

### Streaming (`/mcp/stream/{tool}`)
- **Use when:** You want real-time progress updates
- **Response:** Server-Sent Events with progress, then result
- **Best for:** UIs, long-running conversions, user feedback

---

## 🚀 Production Deployment

### Using systemd

Create `/etc/systemd/system/mcp-http.service`:

```ini
[Unit]
Description=MarkItDown MCP HTTP Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/local-mcpserver
ExecStart=/path/to/local-mcpserver/.venv/bin/python markitdown_server/mcp_http_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Commands:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable mcp-http
sudo systemctl start mcp-http
sudo systemctl status mcp-http
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY markitdown_server/mcp_http_server.py .

EXPOSE 8002

CMD ["python", "mcp_http_server.py"]
```

**Build and run:**
```bash
docker build -t mcp-http-server .
docker run -d -p 8002:8002 --name mcp-http mcp-http-server
```

### Behind nginx

```nginx
server {
    listen 80;
    server_name mcp.yourdomain.com;

    location / {
        proxy_pass http://localhost:8002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        
        # For SSE streaming
        proxy_buffering off;
        proxy_read_timeout 86400;
    }
}
```

---

## 🔒 Security

### API Authentication (Optional)

Add authentication to the server:

```python
from fastapi import Depends, HTTPException, Header

async def verify_token(x_api_key: str = Header(...)):
    if x_api_key != "your-secret-token":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# Apply to endpoints
@app.post("/mcp/call/{tool_name}", dependencies=[Depends(verify_token)])
async def call_tool(tool_name: str, args: dict):
    ...
```

**Usage:**
```bash
curl -X POST http://localhost:8002/mcp/call/convert_file \
  -H "X-API-Key: your-secret-token" \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/file.pdf"}'
```

### CORS Configuration

Already configured in the server for all origins. For production, restrict to specific domains:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧪 Testing

### Test with Python
```bash
python << 'EOF'
import requests
resp = requests.post(
    "http://localhost:8002/mcp/call/get_supported_formats",
    json={}
)
print(resp.json())
EOF
```

### Test Streaming
```bash
curl -N -X POST http://localhost:8002/mcp/stream/get_supported_formats \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Upload Test File
```bash
echo "# Test Document" > /tmp/test.txt
curl -N -X POST http://localhost:8002/mcp/upload \
  -F "file=@/tmp/test.txt"
```

---

## 🔧 Troubleshooting

### Server won't start
```bash
# Check if port is in use
lsof -i :8002

# Kill existing process
pkill -f mcp_http_server

# Check Python path
which python
.venv/bin/python --version
```

### Connection refused
```bash
# Verify server is running
curl http://localhost:8002/health

# Check firewall
sudo ufw status
sudo ufw allow 8002
```

### Streaming not working
- Ensure you're using `-N` flag with curl for streaming
- Check that `proxy_buffering off` is set in nginx
- Verify client supports Server-Sent Events

---

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8002/health
```

### Logs
```bash
# If running with systemd
journalctl -u mcp-http -f

# If running directly
# Logs appear in terminal
```

### Metrics (Optional)

Add Prometheus metrics:

```python
from prometheus_client import Counter, Histogram, generate_latest

conversions = Counter('mcp_conversions_total', 'Total conversions')
conversion_duration = Histogram('mcp_conversion_duration_seconds', 'Conversion duration')

@app.get("/metrics")
async def metrics():
    return generate_latest()
```

---

## 🎯 Use Cases

1. **Web Applications** - Integrate document conversion into your web app
2. **Mobile Apps** - Convert documents from mobile devices
3. **Automation Scripts** - Batch process documents via HTTP
4. **Microservices** - Use as a conversion microservice
5. **AI Assistants** - Let AI assistants call via HTTP instead of STDIO
6. **APIs** - Expose conversion capabilities via your API

---

## 📞 Support

- Check [README.md](../README.md) for general setup
- See [WEB_SERVER_GUIDE.md](WEB_SERVER_GUIDE.md) for web UI guide
- Open issues on [GitHub](https://github.com/majidraza1228/local-mcpserver/issues)
