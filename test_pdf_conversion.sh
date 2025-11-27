#!/bin/bash

# Test MCP Server - PDF Conversion
# Run this script to test your MCP server

echo "======================================"
echo "MCP Server Testing Guide"
echo "======================================"
echo ""

# Check if server is running
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Server is running on http://localhost:8080"
else
    echo "❌ Server is NOT running"
    echo ""
    echo "Start the server first:"
    echo "  ./markitdown_server/start_http_streaming.sh"
    echo ""
    echo "Or run this in a separate terminal:"
    echo "  cd /Users/syedraza/mcp-local"
    echo "  .venv/bin/python markitdown_server/http_streaming_server.py"
    exit 1
fi

echo ""
echo "======================================"
echo "Test 1: List Available Tools"
echo "======================================"
curl -s http://localhost:8080/api/tools | python3 -m json.tool

echo ""
echo "======================================"
echo "Test 2: Get Supported Formats"
echo "======================================"
curl -s http://localhost:8080/api/formats | python3 -m json.tool

echo ""
echo "======================================"
echo "Test 3: Convert PDF File"
echo "======================================"
PDF_PATH="/Users/syedraza/Documents/markitdown/fast-api.pdf"

if [ -f "$PDF_PATH" ]; then
    echo "Converting: $PDF_PATH"
    echo ""
    
    # Method 1: Using convert_file (if file exists on server)
    echo "Method 1: Using MCP convert_file tool"
    curl -s -X POST http://localhost:8080/api/call/convert_file \
      -H "Content-Type: application/json" \
      -d "{\"path\":\"$PDF_PATH\"}" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'result' in data:
        print('✅ Conversion successful!')
        print('')
        result = data['result']
        # Print first 500 characters
        print('Preview (first 500 chars):')
        print('-' * 50)
        print(result[:500] if len(result) > 500 else result)
        print('...' if len(result) > 500 else '')
        print('')
        print(f'Total length: {len(result)} characters')
    else:
        print('❌ Error:', data)
except Exception as e:
    print('❌ Error parsing response:', e)
"
else
    echo "⚠️  File not found: $PDF_PATH"
    echo ""
    echo "Method 2: Upload a PDF file"
    echo "Run this command with your own PDF:"
    echo ""
    echo "  curl -N -X POST http://localhost:8080/api/stream/convert \\"
    echo "    -F 'file=@/path/to/your/file.pdf'"
fi

echo ""
echo "======================================"
echo "Test 4: Convert URL"
echo "======================================"
echo "Converting: https://example.com"
curl -s -X POST http://localhost:8080/api/call/convert_url \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'result' in data:
        print('✅ URL conversion successful!')
        print('')
        result = data['result']
        print('Preview (first 300 chars):')
        print('-' * 50)
        print(result[:300])
        print('...')
    else:
        print('❌ Error:', data)
except: pass
"

echo ""
echo "======================================"
echo "Additional Testing Methods"
echo "======================================"
echo ""
echo "1. Web UI:"
echo "   open http://localhost:8080"
echo "   Then drag-and-drop your PDF file"
echo ""
echo "2. Upload via API:"
echo "   curl -N -X POST http://localhost:8080/api/stream/convert \\"
echo "     -F 'file=@/path/to/your/file.pdf'"
echo ""
echo "3. VS Code Copilot (Traditional MCP):"
echo "   Restart VS Code and use:"
echo "   @workspace Convert /path/to/file.pdf to markdown"
echo ""
echo "4. MCP Inspector:"
echo "   npx @modelcontextprotocol/inspector \\"
echo "     /Users/syedraza/mcp-local/.venv/bin/python \\"
echo "     /Users/syedraza/mcp-local/markitdown_server/server.py"
echo ""
echo "======================================"
