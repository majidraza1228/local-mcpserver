#!/bin/bash

# Traditional MCP Communication Example (STDIO)
# This shows how AI assistants communicate with MCP servers

echo "======================================"
echo "Traditional MCP Protocol Test (STDIO)"
echo "======================================"
echo ""

# Configuration
MCP_SERVER="/Users/syedraza/mcp-local/.venv/bin/python"
MCP_SCRIPT="/Users/syedraza/mcp-local/markitdown_server/server.py"

echo "1. Testing: List supported formats"
echo "--------------------------------------"
echo "Sending MCP request..."

# MCP protocol message (JSON-RPC 2.0)
REQUEST='{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_supported_formats","arguments":{}}}'

# Send via STDIO and get response
RESPONSE=$(echo "$REQUEST" | "$MCP_SERVER" "$MCP_SCRIPT" 2>/dev/null | grep -v "^[^{]")

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo ""

echo "2. Testing: Convert URL to Markdown"
echo "--------------------------------------"
echo "Sending MCP request to convert https://example.com..."

REQUEST='{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"convert_url","arguments":{"url":"https://example.com"}}}'

RESPONSE=$(echo "$REQUEST" | "$MCP_SERVER" "$MCP_SCRIPT" 2>/dev/null | grep -v "^[^{]")

echo "Response (first 300 chars):"
echo "$RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('result', {}).get('content', str(d))[:300])" 2>/dev/null || echo "Check server.py output"
echo ""

echo "3. Testing: Convert PDF file"
echo "--------------------------------------"
echo "To convert a PDF file, use this format:"
echo ""
echo 'REQUEST='"'"'{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"convert_file","arguments":{"path":"/absolute/path/to/your/file.pdf"}}}'"'"
echo 'echo "$REQUEST" | '"$MCP_SERVER"' '"$MCP_SCRIPT"
echo ""

echo "======================================"
echo "Traditional MCP Examples Complete!"
echo "======================================"
echo ""
echo "This is EXACTLY how VS Code Copilot communicates with MCP servers:"
echo "  1. Sends JSON-RPC request via STDIN"
echo "  2. Receives JSON-RPC response via STDOUT"
echo "  3. All communication is text-based protocol"
echo ""
echo "To use with VS Code Copilot:"
echo "  1. Edit ~/.config/mcp/config.json"
echo "  2. Add server configuration"
echo "  3. Restart VS Code"
echo "  4. Use: @workspace Convert document.pdf to markdown"
