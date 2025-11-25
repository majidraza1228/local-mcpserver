#!/usr/bin/env python3
"""Example: Create a PR using the GitHub MCP server"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os

async def create_pr_example():
    """Demonstrate creating a PR workflow"""
    
    # Server parameters
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
            print("GitHub PR Creation Example")
            print("=" * 60)
            print()
            
            owner = "majidraza1228"
            repo = "local-mcpserver"
            
            # Step 1: List existing branches
            print("Step 1: Listing branches...")
            result = await session.call_tool("list_branches", arguments={"owner": owner, "repo": repo})
            data = json.loads(result.content[0].text)
            print(f"Found {data['count']} branches:")
            for branch in data['branches'][:5]:
                print(f"  - {branch['name']}")
            print()
            
            # Step 2: Create a new branch
            branch_name = "feature/add-pr-tools"
            print(f"Step 2: Creating new branch '{branch_name}'...")
            result = await session.call_tool(
                "create_branch",
                arguments={
                    "owner": owner,
                    "repo": repo,
                    "branch_name": branch_name,
                    "from_branch": "master"
                }
            )
            data = json.loads(result.content[0].text)
            if data.get("success"):
                print(f"✓ {data['message']}")
            else:
                print(f"Note: {data.get('error', 'Branch might already exist')}")
            print()
            
            # Step 3: Create/Update a file
            print("Step 3: Creating a new file in the branch...")
            new_content = """# PR Tools Added

This branch demonstrates the new PR creation tools added to the GitHub server:

- create_branch
- create_or_update_file
- get_file_content
- create_pull_request
- list_branches

These tools enable full PR workflow automation!
"""
            result = await session.call_tool(
                "create_or_update_file",
                arguments={
                    "owner": owner,
                    "repo": repo,
                    "path": "docs/PR_TOOLS.md",
                    "content": new_content,
                    "message": "Add documentation for PR tools",
                    "branch": branch_name
                }
            )
            data = json.loads(result.content[0].text)
            if data.get("success"):
                print(f"✓ {data['message']}")
            else:
                print(f"Error: {data.get('error')}")
                print(f"Message: {data.get('message')}")
            print()
            
            # Step 4: Create Pull Request
            print("Step 4: Creating pull request...")
            pr_body = """## What's Changed

Added comprehensive GitHub PR creation tools to the MCP server:

### New Tools
- **create_branch**: Create new branches from existing ones
- **create_or_update_file**: Create or modify files in the repository
- **get_file_content**: Retrieve file contents
- **create_pull_request**: Create PRs programmatically
- **list_branches**: List all repository branches

### Benefits
- Automate PR workflows
- Create branches and files programmatically
- Full GitHub integration via MCP

This PR demonstrates the new functionality by adding itself!
"""
            result = await session.call_tool(
                "create_pull_request",
                arguments={
                    "owner": owner,
                    "repo": repo,
                    "title": "Add PR creation tools to GitHub MCP server",
                    "head": branch_name,
                    "base": "master",
                    "body": pr_body
                }
            )
            data = json.loads(result.content[0].text)
            if data.get("success"):
                print(f"✓ Pull Request created successfully!")
                print(f"  PR #{data['number']}: {data['title']}")
                print(f"  URL: {data['url']}")
                print(f"  State: {data['state']}")
            else:
                print(f"Error: {data.get('error')}")
                print(f"Message: {data.get('message')}")
            print()
            
            print("=" * 60)
            print("✓ PR workflow completed!")
            print("=" * 60)

if __name__ == "__main__":
    if not os.environ.get('GITHUB_TOKEN'):
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Run: export GITHUB_TOKEN=your_token_here")
        exit(1)
    
    asyncio.run(create_pr_example())
