#!/bin/bash

# Setup Helper Script
# This script helps developers set up the MCP server configuration

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}MCP Server Local Setup Helper${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Get project directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo -e "${BLUE}Project directory:${NC} $PROJECT_DIR"
echo ""

# Check if virtual environment exists
if [ ! -d "$PROJECT_DIR/.venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
    echo ""
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$PROJECT_DIR/.venv/bin/activate"
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --quiet --upgrade pip
pip install --quiet fastmcp markitdown fastapi uvicorn python-multipart sqlalchemy watchdog
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Verify installation
echo -e "${YELLOW}Verifying installation...${NC}"
python -c "import fastmcp, markitdown, fastapi; print('✓ All imports successful')"
echo ""

# Create MCP config directory
MCP_CONFIG_DIR="$HOME/.config/mcp"
MCP_CONFIG_FILE="$MCP_CONFIG_DIR/config.json"

echo -e "${YELLOW}MCP Configuration:${NC}"
echo -e "${BLUE}Config location:${NC} $MCP_CONFIG_FILE"
echo ""

# Check if config already exists
if [ -f "$MCP_CONFIG_FILE" ]; then
    echo -e "${YELLOW}⚠️  MCP config file already exists${NC}"
    echo ""
    read -p "Do you want to update it? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing config"
        SKIP_CONFIG=true
    fi
fi

if [ "$SKIP_CONFIG" != "true" ]; then
    # Create config directory if it doesn't exist
    mkdir -p "$MCP_CONFIG_DIR"
    
    # Create config file
    cat > "$MCP_CONFIG_FILE" << EOF
{
  "version": "1.0",
  "servers": {
    "markitdown": {
      "command": "$PROJECT_DIR/.venv/bin/python",
      "args": ["./markitdown_server/server.py"],
      "cwd": "$PROJECT_DIR",
      "description": "Convert documents (PDF, DOCX, XLSX, etc.) to Markdown"
    },
    "database": {
      "command": "$PROJECT_DIR/.venv/bin/python",
      "args": ["./db_server/server.py"],
      "cwd": "$PROJECT_DIR",
      "env": {
        "DB_PATH": "$HOME/database.db"
      },
      "description": "Query SQLite databases safely"
    }
  }
}
EOF
    
    echo -e "${GREEN}✓ MCP config file created${NC}"
    echo ""
fi

# Show config
echo -e "${YELLOW}Current MCP Configuration:${NC}"
cat "$MCP_CONFIG_FILE"
echo ""

# Test servers
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Restart VS Code completely (Cmd+Q on macOS)"
echo ""
echo "2. Test in VS Code Copilot:"
echo "   @workspace List available MCP tools"
echo "   @workspace What file formats can you convert?"
echo ""
echo "3. Or start HTTP server:"
echo "   cd $PROJECT_DIR"
echo "   ./markitdown_server/start_http_streaming.sh"
echo "   # Then visit http://localhost:8080"
echo ""
echo -e "${BLUE}Configuration file:${NC} $MCP_CONFIG_FILE"
echo -e "${BLUE}Project directory:${NC} $PROJECT_DIR"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
