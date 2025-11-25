# Local MCP Server

A collection of Model Context Protocol (MCP) servers for database access, GitHub integration, and markdown conversion. Use with VS Code & GitHub Copilot for AI-powered development workflows.

## 🚀 Quick Start with VS Code

### 1. Install Prerequisites
```bash
# Clone the repository
git clone https://github.com/majidraza1228/local-mcpserver.git
cd local-mcpserver

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or .venv\Scripts\activate on Windows

# Install dependencies
pip install fastmcp sqlalchemy requests mcp
```

### 2. Configure VS Code

Create `.vscode/settings.json` in your workspace:
```json
{
  "github.copilot.chat.mcp.servers": {
    "github-tools": {
      "command": "/absolute/path/to/local-mcpserver/.venv/bin/python",
      "args": ["/absolute/path/to/local-mcpserver/github_server/server.py"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "database-tools": {
      "command": "/absolute/path/to/local-mcpserver/.venv/bin/python",
      "args": ["/absolute/path/to/local-mcpserver/db_server/server.py"],
      "env": {
        "DB_DSN": "sqlite+pysqlite:///./app.db",
        "DB_READONLY": "1"
      }
    }
  }
}
```

### 3. Set GitHub Token
```bash
# Get token from https://github.com/settings/tokens
export GITHUB_TOKEN=your_github_personal_access_token
```

### 4. Use with GitHub Copilot Chat

Open Copilot Chat (⌘+Shift+I / Ctrl+Shift+I) and try:
```
@workspace List all branches in my repository

@workspace Create a branch called feature/new-feature from master

@workspace Create a PR from feature/new-feature to master
```

**[📖 Full VS Code Integration Guide](VSCODE_INTEGRATION.md)**

## Overview

This repository contains three FastMCP servers that provide different functionalities through the MCP protocol:

1. **Database Server** - Safe SQLite database access with read/write controls
2. **GitHub Server** - GitHub API integration for repository operations, PR creation, and branch management
3. **Markitdown Server** - Document conversion to markdown format

## Features

### GitHub Server
- ✅ Repository information and search
- ✅ Issue listing and management
- ✅ Branch creation and listing
- ✅ File creation and updates
- ✅ Pull request creation
- ✅ Full GitHub API integration

### Database Server
- ✅ Safe SQLite access with read-only mode
- ✅ Schema inspection
- ✅ Table listing and preview
- ✅ Parameterized SQL queries with safety controls

### Use Cases
- **Automate PR workflows** - Create branches, update files, and create PRs through chat
- **Database exploration** - Query databases naturally with AI assistance
- **Repository management** - Manage GitHub repositories through natural language
- **Development automation** - Automate repetitive development tasks

## Prerequisites

- Python 3.10 or higher
- pipenv (recommended) or pip
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/majidraza1228/local-mcpserver.git
cd local-mcpserver
```

### 2. Set Up Virtual Environment

Using pipenv (recommended):
```bash
pipenv install
pipenv shell
```

Or using pip:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

pip install fastmcp sqlalchemy requests
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Database Configuration
DB_DSN=sqlite+pysqlite:///./app.db
DB_READONLY=1
DB_MAX_ROWS=1000

# GitHub Configuration (get your token from https://github.com/settings/tokens)
GITHUB_TOKEN=your_github_personal_access_token
```

**Note:** Never commit your `.env` file to git. It's already included in `.gitignore`.

Load environment variables (bash/zsh):
```bash
export GITHUB_TOKEN=your_github_personal_access_token
```

## Servers

### 1. Database Server (`db_server/server.py`)

Provides safe SQLite database access with configurable read/write permissions.

#### Features
- Schema inspection via resource endpoint
- Table listing
- Row preview with pagination
- Parameterized SQL queries with safety controls

#### Tools
- `db_tables()` - List all tables in the database
- `db_preview(table, limit)` - Preview first N rows from a table
- `db_query(sql, params, max_rows)` - Execute parameterized SQL queries

#### Resources
- `resource://db/schema` - Database schema information in markdown format

#### Usage
```bash
python db_server/server.py
```

#### Configuration
- `DB_DSN` - Database connection string (default: `sqlite+pysqlite:///./app.db`)
- `DB_READONLY` - Enable read-only mode (default: `1`)
- `DB_MAX_ROWS` - Maximum rows returned per query (default: `1000`)

### 2. GitHub Server (`github_server/server.py`)

Integrates with GitHub API to provide repository information and operations.

#### Features
- Repository information retrieval
- Issue listing and filtering
- Repository search

#### Tools
- `get_repo_info(owner, repo)` - Get detailed information about a repository
- `list_issues(owner, repo, state, limit)` - List issues from a repository
- `search_repos(query, limit)` - Search GitHub repositories
- `create_branch(owner, repo, branch_name, from_branch)` - Create a new branch
- `create_or_update_file(owner, repo, path, content, message, branch, sha)` - Create or update files
- `get_file_content(owner, repo, path, branch)` - Get file content from repository
- `create_pull_request(owner, repo, title, head, base, body)` - Create a pull request
- `list_branches(owner, repo, limit)` - List all branches in a repository

#### Usage
```bash
python github_server/server.py
```

#### Configuration
- `GITHUB_TOKEN` - GitHub personal access token (optional but recommended for higher rate limits)

#### Example Queries
```python
# Get repository info
get_repo_info(owner="majidraza1228", repo="local-mcpserver")

# List open issues
list_issues(owner="majidraza1228", repo="local-mcpserver", state="open", limit=20)

# Search repositories
search_repos(query="machine learning python", limit=10)

# Create a new branch
create_branch(owner="majidraza1228", repo="local-mcpserver", branch_name="feature/new-feature", from_branch="master")

# Create or update a file
create_or_update_file(
    owner="majidraza1228",
    repo="local-mcpserver",
    path="README.md",
    content="# Updated content",
    message="Update README",
    branch="feature/new-feature"
)

# Create a pull request
create_pull_request(
    owner="majidraza1228",
    repo="local-mcpserver",
    title="Add new feature",
    head="feature/new-feature",
    base="master",
    body="Description of changes"
)
```

#### Complete PR Creation Example

See `example_create_pr.py` for a full workflow example that:
1. Lists existing branches
2. Creates a new feature branch
3. Adds/updates files in the branch
4. Creates a pull request

Run it with:
```bash
export GITHUB_TOKEN=your_token
python example_create_pr.py
```

### 3. Markitdown Server (`markitdown_server/server.py`)

Converts various document formats to markdown.

#### Usage
```bash
python markitdown_server/server.py
```

## Running the Servers

Each server runs independently using the STDIO transport protocol for MCP communication.

### Prerequisites
- Ensure virtual environment is activated
- Set required environment variables (especially `GITHUB_TOKEN` for GitHub server)

### Running Locally

#### Database Server
```bash
# Using full path to venv python
/path/to/local-mcpserver/.venv/bin/python ./db_server/server.py

# Or if venv is activated
python3 ./db_server/server.py
```

#### GitHub Server
```bash
# Set GitHub token first
export GITHUB_TOKEN=your_github_personal_access_token

# Run the server
/path/to/local-mcpserver/.venv/bin/python ./github_server/server.py

# Or if venv is activated
python3 ./github_server/server.py
```

#### Markitdown Server
```bash
/path/to/local-mcpserver/.venv/bin/python ./markitdown_server/server.py
```

**Note:** Servers run in STDIO mode and wait for MCP protocol messages. They won't show output until they receive input from an MCP client.

## Using with VS Code & GitHub Copilot (Like Copilot Chat)

To use these servers with VS Code and GitHub Copilot for natural language interactions, see the detailed integration guide:

**[📖 VS Code & GitHub Copilot Integration Guide](VSCODE_INTEGRATION.md)**

This enables you to use GitHub Copilot Chat to:
- Create branches and PRs
- Update files in your repository  
- Query your database
- Search repositories
- And more - all through natural conversation!

## Testing the Servers

### Option 1: Unit Tests (GitHub API Direct Testing)

Test the GitHub API functionality without MCP:

```bash
# Run the API test script
python test_github_server.py
```

This will test:
- GitHub API authentication and rate limits
- Repository information retrieval
- Issue listing
- Repository search

Expected output:
```
============================================================
GitHub Server Functionality Test
============================================================

Checking GitHub API rate limit...
✓ Rate Limit: 4999/5000
  Authenticated: Yes

Testing get_repo_info...
✓ Repository: majidraza1228/local-mcpserver
  Description: Local MCP servers for database and GitHub integration
```

### Option 2: MCP Client Test (Full Integration Testing)

Test the server through the MCP protocol:

```bash
# Install MCP client library (if not already installed)
pip install mcp

# Run the MCP client test
python test_mcp_client.py
```

This will:
1. Start the GitHub server as a subprocess
2. Connect via MCP protocol
3. Test all available tools (get_repo_info, list_issues, search_repos)
4. Display results and verify functionality

Expected output:
```
============================================================
Connected to GitHub MCP Server
============================================================

Available tools: 3
  - get_repo_info: Get information about a GitHub repository
  - list_issues: List recent issues for a GitHub repository
  - search_repos: Search GitHub repositories

Test 1: Getting repository info...
Result: {
  "name": "local-mcpserver",
  "full_name": "majidraza1228/local-mcpserver",
  ...
}
```

### Option 3: MCP Inspector (Interactive Testing)

Use the official MCP Inspector for interactive testing:

```bash
npx @modelcontextprotocol/inspector \
  /path/to/local-mcpserver/.venv/bin/python \
  /path/to/local-mcpserver/github_server/server.py
```

This opens a web interface where you can:
- View all available tools and resources
- Test tools interactively with custom parameters
- See real-time request/response logs

### Using with MCP Clients

These servers are designed to work with MCP-compatible clients. The servers communicate via standard input/output (STDIO transport).

Example client configuration (for Claude Desktop or similar):
```json
{
  "mcpServers": {
    "database": {
      "command": "/path/to/local-mcpserver/.venv/bin/python",
      "args": ["/path/to/local-mcpserver/db_server/server.py"],
      "env": {
        "DB_DSN": "sqlite+pysqlite:///./app.db",
        "DB_READONLY": "1"
      }
    },
    "github": {
      "command": "/path/to/local-mcpserver/.venv/bin/python",
      "args": ["/path/to/local-mcpserver/github_server/server.py"],
      "env": {
        "GITHUB_TOKEN": "your_github_personal_access_token"
      }
    }
  }
}
```

## Project Structure

```
local-mcpserver/
├── db_server/
│   └── server.py              # Database MCP server
├── github_server/
│   └── server.py              # GitHub API MCP server
├── markitdown_server/
│   └── server.py              # Markitdown conversion server
├── test_github_server.py      # GitHub API unit tests
├── test_mcp_client.py         # MCP integration tests
├── example_create_pr.py       # Example: Create PR workflow
├── .env                       # Environment variables (not in git)
├── .gitignore                 # Git ignore file
├── Pipfile                    # Python dependencies (pipenv)
├── Pipfile.lock              # Locked dependencies
└── README.md                  # This file
```

## Dependencies

- **fastmcp** (>=2.13.1) - FastMCP framework for building MCP servers
- **sqlalchemy** - Database toolkit and ORM
- **requests** - HTTP library for GitHub API calls

## Security Considerations

### Database Server
- Read-only mode is enabled by default (`DB_READONLY=1`)
- Write operations (INSERT, UPDATE, DELETE, etc.) are blocked in read-only mode
- Query results are capped to prevent memory issues
- Use parameterized queries to prevent SQL injection

### GitHub Server
- Store your GitHub token securely in `.env` file
- Never commit `.env` file to version control
- Token provides authenticated access and higher rate limits
- Respects GitHub API rate limits

## Troubleshooting

### Import Errors
If you get `ModuleNotFoundError`, ensure you're using the virtual environment:
```bash
# Check which Python is being used
which python

# Should point to .venv/bin/python
# If not, activate the virtual environment
source .venv/bin/activate
```

### Database Connection Issues
- Verify the `DB_DSN` connection string is correct
- Check file permissions for SQLite database file
- Ensure SQLite driver is installed: `pip install sqlalchemy`

### GitHub API Rate Limiting
- Without authentication: 60 requests/hour
- With authentication: 5,000 requests/hour
- Set `GITHUB_TOKEN` environment variable with a personal access token

### Server Not Starting
Ensure all dependencies are installed:
```bash
pip install fastmcp sqlalchemy requests
```

## Development

### Adding New Tools

To add a new tool to any server:

```python
@app.tool(description="Your tool description")
def your_tool_name(param1: str, param2: int = 10):
    """Tool documentation."""
    # Your implementation
    return {"result": "data"}
```

### Adding New Resources

To add a new resource:

```python
@app.resource(uri="resource://your/path", mime_type="text/plain")
def your_resource():
    """Resource documentation."""
    return "resource content"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

## License

MIT License - feel free to use this code for your projects.

## Resources

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the FastMCP documentation

## Changelog

### v1.0.0 (2024-11-24)
- Initial release
- Database server with SQLite support
- GitHub server with repository and issue tools
- Markitdown server for document conversion
