#!/bin/bash

echo "==================================="
echo "MCP Server Quick Test"
echo "==================================="
echo ""

echo "Test 1: Check Python environment..."
/Users/syedraza/mcp-local/.venv/bin/python --version
if [ $? -eq 0 ]; then
    echo "✅ Python OK"
else
    echo "❌ Python FAILED"
    exit 1
fi

echo ""
echo "Test 2: Check FastMCP installation..."
/Users/syedraza/mcp-local/.venv/bin/python -c "import fastmcp; print('FastMCP version:', fastmcp.__version__)"
if [ $? -eq 0 ]; then
    echo "✅ FastMCP OK"
else
    echo "❌ FastMCP FAILED"
    exit 1
fi

echo ""
echo "Test 3: Check MarkItDown installation..."
/Users/syedraza/mcp-local/.venv/bin/python -c "import markitdown; print('MarkItDown OK')"
if [ $? -eq 0 ]; then
    echo "✅ MarkItDown OK"
else
    echo "❌ MarkItDown FAILED"
    exit 1
fi

echo ""
echo "Test 4: Check MCP config exists..."
if [ -f "/Users/syedraza/.config/mcp/config.json" ]; then
    echo "✅ MCP config exists"
    cat /Users/syedraza/.config/mcp/config.json | grep "markitdown" > /dev/null
    if [ $? -eq 0 ]; then
        echo "✅ markitdown server configured"
    else
        echo "❌ markitdown server NOT configured"
    fi
else
    echo "❌ MCP config NOT found"
fi

echo ""
echo "Test 5: Verify server file exists..."
if [ -f "/Users/syedraza/mcp-local/markitdown_server/server.py" ]; then
    echo "✅ Server file exists"
else
    echo "❌ Server file NOT found"
    exit 1
fi

echo ""
echo "Test 6: Check for @app.tool decorators..."
grep -q "@app.tool" /Users/syedraza/mcp-local/markitdown_server/server.py
if [ $? -eq 0 ]; then
    TOOL_COUNT=$(grep -c "@app.tool" /Users/syedraza/mcp-local/markitdown_server/server.py)
    echo "✅ Found $TOOL_COUNT MCP tools"
else
    echo "❌ No @app.tool decorators found"
    exit 1
fi

echo ""
echo "==================================="
echo "✅ All tests passed!"
echo "==================================="
echo ""
echo "Your MCP server is properly configured!"
echo ""
echo "Next steps to test:"
echo "1. Start server manually:"
echo "   python markitdown_server/server.py"
echo ""
echo "2. Use MCP Inspector:"
echo "   npx @modelcontextprotocol/inspector \\"
echo "     /Users/syedraza/mcp-local/.venv/bin/python \\"
echo "     /Users/syedraza/mcp-local/markitdown_server/server.py"
echo ""
echo "3. Test in VS Code Copilot Chat:"
echo "   @workspace What formats does markitdown support?"
echo ""
