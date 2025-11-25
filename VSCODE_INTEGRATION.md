# Integrating with VS Code and GitHub Copilot

This guide shows how to integrate the local MCP servers with VS Code and GitHub Copilot, enabling you to use GitHub tools directly in your editor.

## What This Enables

Once configured, you can use GitHub Copilot Chat to:
- "List all branches in my repository"
- "Create a new branch called feature/add-tests"
- "Update the README file"
- "Create a PR for my changes"
- "Show me the database tables"

GitHub Copilot will use the MCP tools to fulfill your requests!

## Prerequisites

1. **VS Code** installed
2. **GitHub Copilot** subscription (individual, business, or enterprise)
3. **GitHub Copilot Chat** extension installed in VS Code

## Configuration for VS Code

### Option 1: Using GitHub Copilot with MCP (Recommended)

GitHub Copilot now supports MCP servers through workspace configuration.

#### Step 1: Create VS Code Settings

Create or edit `.vscode/settings.json` in your workspace:

```json
{
  "github.copilot.chat.mcp.servers": {
    "github-tools": {
      "command": "/Users/syedraza/mcp-local/.venv/bin/python",
      "args": ["/Users/syedraza/mcp-local/github_server/server.py"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "database-tools": {
      "command": "/Users/syedraza/mcp-local/.venv/bin/python",
      "args": ["/Users/syedraza/mcp-local/db_server/server.py"],
      "env": {
        "DB_DSN": "sqlite+pysqlite:///./app.db",
        "DB_READONLY": "1",
        "DB_MAX_ROWS": "1000"
      }
    }
  }
}
```

**Note:** Update the paths to match your actual installation location.

#### Step 2: Set Environment Variables

Create a `.env` file in your workspace root (already gitignored):

```bash
GITHUB_TOKEN=your_github_personal_access_token
```

Or set it in your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export GITHUB_TOKEN=your_github_personal_access_token
```

Reload VS Code after setting environment variables.

### Option 2: Using Continue.dev Extension

Continue.dev is an alternative that provides excellent MCP support.

#### Step 1: Install Continue Extension

1. Open VS Code
2. Go to Extensions (⌘+Shift+X)
3. Search for "Continue"
4. Install the extension

#### Step 2: Configure Continue

Create or edit `~/.continue/config.json`:

```json
{
  "models": [
    {
      "title": "GPT-4",
      "provider": "openai",
      "model": "gpt-4",
      "apiKey": "your-openai-api-key"
    }
  ],
  "mcpServers": {
    "github-tools": {
      "command": "/Users/syedraza/mcp-local/.venv/bin/python",
      "args": ["/Users/syedraza/mcp-local/github_server/server.py"],
      "env": {
        "GITHUB_TOKEN": "your_github_token"
      }
    },
    "database-tools": {
      "command": "/Users/syedraza/mcp-local/.venv/bin/python",
      "args": ["/Users/syedraza/mcp-local/db_server/server.py"],
      "env": {
        "DB_DSN": "sqlite+pysqlite:///./app.db",
        "DB_READONLY": "1"
      }
    }
  }
}
```

## Get Your GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:org`, `workflow`
4. Generate and copy the token
5. Add it to your configuration

## Usage Examples

### Using GitHub Copilot Chat

Open Copilot Chat (⌘+Shift+I or Ctrl+Shift+I) and try:

```
@workspace List all branches in my local-mcpserver repository
```

```
@workspace Create a new branch called feature/add-tests from master
```

```
@workspace Show me the contents of README.md
```

```
@workspace Create a PR from feature/add-tests to master with title "Add test suite"
```

### Using Continue.dev

Click the Continue icon in the sidebar (or ⌘+L) and ask:

```
List all my GitHub repositories
```

```
Create a new file called test.py in branch feature/testing
```

```
What tables are in my database?
```

```
Query the users table for all active users
```

## Verify Integration

### Check MCP Servers are Running

1. Open VS Code terminal
2. Run:
```bash
export GITHUB_TOKEN=your_token
/Users/syedraza/mcp-local/.venv/bin/python /Users/syedraza/mcp-local/github_server/server.py
```

You should see:
```
╭──────────────────────────────────────────╮
│         FastMCP 2.13.1                   │
│         Server name: github-tools        │
│         Transport: STDIO                 │
╰──────────────────────────────────────────╯
```

Press Ctrl+C to stop.

### Check Available Tools

In Copilot Chat or Continue, ask:
```
What tools do you have access to?
```

You should see tools like:
- get_repo_info
- create_branch
- create_pull_request
- list_issues
- list_branches
- create_or_update_file
- etc.

## Example Workflows

### Creating a Feature Branch and PR

**Chat:**
```
1. Create a branch called feature/add-logging
2. Add a new file utils/logger.py with basic logging setup
3. Update README to mention the new logging utility
4. Create a PR for these changes
```

GitHub Copilot will:
1. Use `create_branch` tool
2. Use `create_or_update_file` tool (twice)
3. Use `create_pull_request` tool
4. Show you the PR URL

### Database Operations

**Chat:**
```
Show me all tables in my database and preview the first 5 rows of each
```

Copilot will:
1. Use `db_tables` tool
2. Use `db_preview` tool for each table
3. Display results in a formatted way

## VS Code Tasks Integration

Create `.vscode/tasks.json` to run servers as background tasks:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start GitHub MCP Server",
      "type": "shell",
      "command": "${workspaceFolder}/.venv/bin/python",
      "args": ["${workspaceFolder}/github_server/server.py"],
      "isBackground": true,
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    },
    {
      "label": "Start Database MCP Server",
      "type": "shell",
      "command": "${workspaceFolder}/.venv/bin/python",
      "args": ["${workspaceFolder}/db_server/server.py"],
      "isBackground": true,
      "problemMatcher": []
    }
  ]
}
```

Run tasks with: Terminal → Run Task → Select server

## Troubleshooting

### Copilot Not Seeing Tools

1. Check VS Code settings have correct paths
2. Verify GITHUB_TOKEN is set in environment
3. Restart VS Code
4. Check VS Code output panel for errors (View → Output → GitHub Copilot)

### Permission Denied Errors

Ensure Python has execute permissions:
```bash
chmod +x /Users/syedraza/mcp-local/.venv/bin/python
```

### Environment Variables Not Loading

- For `.env` file: Install "DotENV" extension
- For shell variables: Restart VS Code after setting them
- Use absolute paths in configuration

### Server Connection Issues

Check server logs:
```bash
# Test the server manually
export GITHUB_TOKEN=your_token
python github_server/server.py
```

## Benefits

✅ **Native VS Code Integration** - Works directly in your editor
✅ **GitHub Copilot Powered** - Natural language understanding
✅ **Context Aware** - Understands your workspace
✅ **Fast Execution** - Local servers, instant responses
✅ **Secure** - Tokens stored locally, never sent to external services

## Advanced: Custom Copilot Instructions

Create `.github/copilot-instructions.md` in your repository:

```markdown
# GitHub MCP Tools

When working with this repository, you have access to MCP tools:

- Use `create_branch` before making changes
- Use `create_or_update_file` to modify files
- Always create PRs using `create_pull_request`
- Use `list_branches` to check existing branches

## Workflow
1. Create feature branch
2. Make changes
3. Create PR with descriptive title and body
```

Copilot will follow these instructions automatically!

## Next Steps

1. Configure VS Code settings
2. Set up your GitHub token
3. Test with simple queries
4. Build custom workflows
5. Create task automation

Enjoy your AI-powered VS Code experience! 🚀
