# Local MCP Server

A collection of Model Context Protocol (MCP) servers for database access, GitHub integration, and markdown conversion.

## Overview

This repository contains three FastMCP servers that provide different functionalities through the MCP protocol:

1. **Database Server** - Safe SQLite database access with read/write controls
2. **GitHub Server** - GitHub API integration for repository information and operations
3. **Markitdown Server** - Document conversion to markdown format

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

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
```

Load environment variables:
```bash
export $(grep -v '^#' .env | xargs)
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

#### Usage
```bash
python github_server/server.py
```

#### Configuration
- `GITHUB_TOKEN` - GitHub personal access token (optional but recommended for higher rate limits)

#### Example Queries
```python
# Get repository info
get_repo_info(owner="fastmcp", repo="fastmcp")

# List open issues
list_issues(owner="fastmcp", repo="fastmcp", state="open", limit=20)

# Search repositories
search_repos(query="machine learning python", limit=10)
```

### 3. Markitdown Server (`markitdown_server/server.py`)

Converts various document formats to markdown.

#### Usage
```bash
python markitdown_server/server.py
```

## Running the Servers

Each server runs independently using the STDIO transport protocol for MCP communication.

### Basic Usage

```bash
# Activate virtual environment
source .venv/bin/activate  # or pipenv shell

# Run a specific server
python db_server/server.py
python github_server/server.py
python markitdown_server/server.py
```

### Using with MCP Clients

These servers are designed to work with MCP-compatible clients. The servers communicate via standard input/output (STDIO transport).

Example client configuration (for Claude Desktop or similar):
```json
{
  "mcpServers": {
    "database": {
      "command": "python",
      "args": ["/path/to/local-mcpserver/db_server/server.py"],
      "env": {
        "DB_DSN": "sqlite+pysqlite:///./app.db",
        "DB_READONLY": "1"
      }
    },
    "github": {
      "command": "python",
      "args": ["/path/to/local-mcpserver/github_server/server.py"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Project Structure

```
local-mcpserver/
├── db_server/
│   └── server.py           # Database MCP server
├── github_server/
│   └── server.py           # GitHub API MCP server
├── markitdown_server/
│   └── server.py           # Markitdown conversion server
├── .env                    # Environment variables (not in git)
├── Pipfile                 # Python dependencies (pipenv)
├── Pipfile.lock           # Locked dependencies
└── README.md              # This file
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
