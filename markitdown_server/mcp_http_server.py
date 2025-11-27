#!/usr/bin/env python3
"""
MarkItDown MCP Server with HTTP Transport
Exposes MCP tools via HTTP/SSE instead of STDIO for streaming responses.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
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
mcp = FastMCP(name="markitdown-http")

markitdown = MarkItDown()

# Supported formats
SUPPORTED_FORMATS = [
    "pdf", "docx", "xlsx", "pptx", "html", "txt",
    "json", "xml", "jpg", "jpeg", "png", "gif", "wav"
]


@mcp.tool()
def convert_file(path: str) -> str:
    """
    Convert a local file to Markdown format.
    
    Args:
        path: Absolute path to the file to convert
        
    Returns:
        Markdown content as string
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    result = markitdown.convert(path)
    return result.text_content


@mcp.tool()
def convert_url(url: str) -> str:
    """
    Convert a web page to Markdown format.
    
    Args:
        url: URL of the web page to convert
        
    Returns:
        Markdown content as string
    """
    result = markitdown.convert(url)
    return result.text_content


@mcp.tool()
def convert_batch(paths: list[str]) -> dict:
    """
    Convert multiple files to Markdown format.
    
    Args:
        paths: List of absolute paths to files
        
    Returns:
        Dictionary mapping paths to their markdown content
    """
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
    """
    Get list of supported file formats.
    
    Returns:
        List of supported file extensions
    """
    return SUPPORTED_FORMATS


# Create FastAPI app for HTTP transport
app = FastAPI(
    title="MarkItDown MCP HTTP Server",
    description="MCP server with HTTP transport and streaming support",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def stream_tool_execution(tool_name: str, args: dict):
    """Stream MCP tool execution with progress updates"""
    try:
        # Send start event
        yield f"data: {json.dumps({'type': 'start', 'tool': tool_name, 'timestamp': datetime.now().isoformat()})}\n\n"
        await asyncio.sleep(0.1)
        
        # Send progress
        yield f"data: {json.dumps({'type': 'progress', 'message': f'Executing {tool_name}...', 'percent': 30})}\n\n"
        await asyncio.sleep(0.1)
        
        # Execute the MCP tool
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
        
        yield f"data: {json.dumps({'type': 'progress', 'message': 'Finalizing...', 'percent': 90})}\n\n"
        await asyncio.sleep(0.1)
        
        # Send result
        yield f"data: {json.dumps({'type': 'complete', 'result': result, 'percent': 100})}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"


@app.get("/")
async def root():
    """API information"""
    return {
        "service": "MarkItDown MCP HTTP Server",
        "version": "1.0.0",
        "transport": "HTTP with SSE streaming",
        "endpoints": {
            "tools": "/mcp/tools - List available MCP tools",
            "call": "/mcp/call/{tool_name} - Call MCP tool (JSON response)",
            "stream": "/mcp/stream/{tool_name} - Call MCP tool (streaming SSE)",
            "upload": "/mcp/upload - Upload and convert file with streaming"
        }
    }


@app.get("/mcp/tools")
async def list_tools():
    """List all available MCP tools"""
    return {
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


@app.post("/mcp/call/{tool_name}")
async def call_tool(tool_name: str, args: dict):
    """Call an MCP tool and return JSON response (non-streaming)"""
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


@app.post("/mcp/stream/{tool_name}")
async def stream_tool(tool_name: str, args: dict):
    """Call an MCP tool with streaming SSE response"""
    return StreamingResponse(
        stream_tool_execution(tool_name, args),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/mcp/upload")
async def upload_and_convert(file: UploadFile = File(...)):
    """Upload a file and convert with streaming progress"""
    
    # Save uploaded file temporarily
    suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    async def stream_upload_conversion():
        try:
            yield f"data: {json.dumps({'type': 'start', 'filename': file.filename})}\n\n"
            await asyncio.sleep(0.1)
            
            yield f"data: {json.dumps({'type': 'progress', 'message': 'Processing upload...', 'percent': 30})}\n\n"
            await asyncio.sleep(0.1)
            
            result = convert_file(tmp_path)
            
            yield f"data: {json.dumps({'type': 'progress', 'message': 'Finalizing...', 'percent': 90})}\n\n"
            await asyncio.sleep(0.1)
            
            yield f"data: {json.dumps({'type': 'complete', 'result': result, 'percent': 100})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    return StreamingResponse(
        stream_upload_conversion(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "transport": "HTTP", "streaming": "enabled"}


if __name__ == "__main__":
    print("🚀 Starting MarkItDown MCP HTTP Server...")
    print("📡 MCP Protocol over HTTP with SSE streaming")
    print("🌐 Server: http://localhost:8002")
    print("\n📋 API Endpoints:")
    print("   GET  / - API documentation")
    print("   GET  /mcp/tools - List MCP tools")
    print("   POST /mcp/call/{tool} - Execute tool (JSON)")
    print("   POST /mcp/stream/{tool} - Execute tool (SSE)")
    print("   POST /mcp/upload - Upload & convert (SSE)")
    print("\nPress Ctrl+C to stop")
    
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")
