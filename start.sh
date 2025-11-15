#!/bin/bash

# Writers Factory Launcher
# Simple script to start both backend and frontend with one command

set -e  # Exit on error

echo "🚀 Starting Writers Factory..."
echo ""

# Color codes for pretty output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Error: Node.js is not installed${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check if backend dependencies are installed
if [ ! -d "factory/venv" ]; then
    echo -e "${YELLOW}⚠️  Backend virtual environment not found${NC}"
    echo -e "${BLUE}📦 Setting up backend...${NC}"
    cd factory
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    echo -e "${GREEN}✅ Backend setup complete${NC}"
    echo ""
fi

# Check if frontend dependencies are installed
if [ ! -d "webapp/frontend-v2/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Frontend dependencies not found${NC}"
    echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
    cd webapp/frontend-v2
    npm install
    cd ../..
    echo -e "${GREEN}✅ Frontend setup complete${NC}"
    echo ""
fi

# Create a temporary directory for PIDs
mkdir -p .tmp
BACKEND_PID_FILE=".tmp/backend.pid"
FRONTEND_PID_FILE=".tmp/frontend.pid"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down Writers Factory...${NC}"

    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        kill $BACKEND_PID 2>/dev/null || true
        rm "$BACKEND_PID_FILE"
    fi

    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        kill $FRONTEND_PID 2>/dev/null || true
        rm "$FRONTEND_PID_FILE"
    fi

    echo -e "${GREEN}✅ Writers Factory stopped${NC}"
    exit 0
}

# Set trap to cleanup on Ctrl+C or exit
trap cleanup SIGINT SIGTERM EXIT

# Start backend
echo -e "${BLUE}🐍 Starting backend server...${NC}"
cd webapp/backend
source ../../factory/venv/bin/activate
python simple_app.py > ../../.tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "../../$BACKEND_PID_FILE"
cd ../..
echo -e "${GREEN}✅ Backend running (PID: $BACKEND_PID)${NC}"

# Wait for backend to be ready
echo -e "${BLUE}⏳ Waiting for backend to be ready...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend ready!${NC}"
        break
    fi
    sleep 1
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ Backend failed to start. Check .tmp/backend.log for errors${NC}"
        exit 1
    fi
done

# Start frontend
echo -e "${BLUE}⚛️  Starting frontend server...${NC}"
cd webapp/frontend-v2
npm run dev > ../../.tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "../../$FRONTEND_PID_FILE"
cd ../..
echo -e "${GREEN}✅ Frontend running (PID: $FRONTEND_PID)${NC}"

# Wait for frontend to be ready
echo -e "${BLUE}⏳ Waiting for frontend to be ready...${NC}"
sleep 3

# Open browser
echo ""
echo -e "${GREEN}✨ Writers Factory is ready!${NC}"
echo ""
echo -e "${BLUE}📝 Application URLs:${NC}"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo ""
echo -e "${BLUE}📋 Logs:${NC}"
echo "   Backend:  .tmp/backend.log"
echo "   Frontend: .tmp/frontend.log"
echo ""
echo -e "${YELLOW}💡 Tip: Press Ctrl+C to stop Writers Factory${NC}"
echo ""

# Open browser automatically (Mac)
if command -v open &> /dev/null; then
    echo -e "${BLUE}🌐 Opening browser...${NC}"
    sleep 2
    open http://localhost:5173
fi

# Keep script running and wait for Ctrl+C
echo -e "${GREEN}✅ Writers Factory is running!${NC}"
echo ""
wait
