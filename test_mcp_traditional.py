#!/usr/bin/env python3
"""
Traditional MCP Protocol Test
This demonstrates how AI assistants communicate with MCP servers via STDIO
"""

import json
import subprocess
import sys

def send_mcp_request(server_command, tool_name, arguments):
    """
    Send MCP protocol request via STDIO (traditional way)
    This is exactly how VS Code Copilot/Claude Desktop communicate
    """
    
    # MCP protocol message format
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    # Start MCP server process
    process = subprocess.Popen(
        server_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send request via STDIN
    request_str = json.dumps(request) + "\n"
    stdout, stderr = process.communicate(input=request_str, timeout=30)
    
    # Parse response
    if stdout:
        for line in stdout.strip().split('\n'):
            try:
                response = json.loads(line)
                if 'result' in response:
                    return response['result']
            except json.JSONDecodeError:
                continue
    
    if stderr:
        print(f"Error: {stderr}", file=sys.stderr)
    
    return None

def main():
    print("=" * 60)
    print("Traditional MCP Protocol Test (STDIO)")
    print("=" * 60)
    print()
    
    # MCP server command
    server_cmd = [
        "/Users/syedraza/mcp-local/.venv/bin/python",
        "/Users/syedraza/mcp-local/markitdown_server/server.py"
    ]
    
    # Example 1: Get supported formats
    print("Test 1: Get supported formats")
    print("-" * 60)
    result = send_mcp_request(server_cmd, "get_supported_formats", {})
    if result:
        print(f"Supported formats: {result}")
    print()
    
    # Example 2: Convert URL
    print("Test 2: Convert URL to Markdown")
    print("-" * 60)
    result = send_mcp_request(
        server_cmd,
        "convert_url",
        {"url": "https://example.com"}
    )
    if result:
        print("Conversion result:")
        print(result[:500] + "..." if len(result) > 500 else result)
    print()
    
    # Example 3: Convert local file (you need to provide a real path)
    print("Test 3: Convert local file")
    print("-" * 60)
    print("To test file conversion, update the path below:")
    print('result = send_mcp_request(server_cmd, "convert_file", {"path": "/path/to/your/file.pdf"})')
    print()
    
    print("=" * 60)
    print("Traditional MCP Protocol Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
