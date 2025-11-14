#!/bin/bash

# Writers Factory Setup Script
# One-time setup to install all dependencies

set -e  # Exit on error

echo "📦 Writers Factory - First-Time Setup"
echo "====================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python
echo -e "${BLUE}🐍 Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
echo ""

# Check Node
echo -e "${BLUE}📦 Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}✅ Node $NODE_VERSION found${NC}"
echo ""

# Setup backend
echo -e "${BLUE}🔧 Setting up backend...${NC}"
cd factory

if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists, skipping creation${NC}"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

cd ..
echo -e "${GREEN}✅ Backend setup complete${NC}"
echo ""

# Setup frontend
echo -e "${BLUE}⚛️  Setting up frontend...${NC}"
cd webapp/frontend-v2

if [ -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  node_modules already exists, skipping installation${NC}"
else
    echo "Installing Node.js dependencies (this may take a few minutes)..."
    npm install
fi

cd ../..
echo -e "${GREEN}✅ Frontend setup complete${NC}"
echo ""

# Create .tmp directory for logs
mkdir -p .tmp

# Check for API keys (optional)
echo -e "${BLUE}🔑 API Keys (Optional)${NC}"
if [ ! -f ".env" ]; then
    echo "No .env file found. You can add API keys later for cloud AI models."
    echo ""
    echo "To use cloud models (Claude, GPT-4, Gemini), create a .env file:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your API keys"
else
    echo -e "${GREEN}✅ .env file found${NC}"
fi
echo ""

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✨ Setup Complete!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}📝 Next Steps:${NC}"
echo ""
echo "1. Start Writers Factory:"
echo -e "   ${YELLOW}./start.sh${NC}"
echo ""
echo "2. Open in browser:"
echo "   http://localhost:5173"
echo ""
echo "3. (Optional) Add API keys for cloud models:"
echo "   - Edit .env file"
echo "   - Add ANTHROPIC_API_KEY, OPENAI_API_KEY, etc."
echo ""
echo "4. (Optional) Install Ollama for local models:"
echo "   https://ollama.ai/"
echo ""
echo -e "${GREEN}Happy writing! ✍️${NC}"
echo ""
