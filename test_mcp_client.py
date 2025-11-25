#!/usr/bin/env python3
"""Simple MCP client to test the GitHub server"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_github_server():
    """Test the GitHub MCP server"""
    
    # Server parameters
    # Get the absolute path to the current directory
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(current_dir, '.venv', 'bin', 'python')
    server_path = os.path.join(current_dir, 'github_server', 'server.py')
    
    server_params = StdioServerParameters(
        command=venv_python,
        args=[server_path],
        env={"GITHUB_TOKEN": os.environ.get('GITHUB_TOKEN', '')}
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            print("=" * 60)
            print("Connected to GitHub MCP Server")
            print("=" * 60)
            print()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()
            
            # Test 1: Get repository info
            print("Test 1: Getting repository info...")
            result = await session.call_tool(
                "get_repo_info",
                arguments={
                    "owner": "majidraza1228",
                    "repo": "local-mcpserver"
                }
            )
            print(f"Result: {json.dumps(json.loads(result.content[0].text), indent=2)}")
            print()
            
            # Test 2: Search repositories
            print("Test 2: Searching repositories...")
            result = await session.call_tool(
                "search_repos",
                arguments={
                    "query": "fastmcp",
                    "limit": 3
                }
            )
            data = json.loads(result.content[0].text)
            print(f"Found {data['total_count']} repositories")
            for repo in data['repositories']:
                print(f"  - {repo['full_name']}: {repo['stars']} stars")
            print()
            
            # Test 3: List issues
            print("Test 3: Listing issues from your repository...")
            result = await session.call_tool(
                "list_issues",
                arguments={
                    "owner": "majidraza1228",
                    "repo": "local-mcpserver",
                    "state": "open",
                    "limit": 5
                }
            )
            data = json.loads(result.content[0].text)
            print(f"Found {data['count']} open issues")
            if data['issues']:
                for issue in data['issues']:
                    print(f"  #{issue['number']}: {issue['title']}")
            else:
                print("  No open issues")
            print()
            
            print("=" * 60)
            print("✓ All MCP tests completed successfully!")
            print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_github_server())
