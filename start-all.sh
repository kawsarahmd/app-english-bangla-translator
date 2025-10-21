#!/bin/bash

# Automated startup script for the entire application
# This script starts all three services in the background

echo "=========================================="
echo "🚀 Starting English-Bangla Translator"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0
    else
        return 1
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local name=$2
    local max_attempts=30
    local attempt=1

    echo -n "Waiting for $name to start..."
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e " ${GREEN}✓${NC}"
            return 0
        fi
        echo -n "."
        sleep 1
        ((attempt++))
    done
    echo -e " ${RED}✗${NC}"
    return 1
}

# Check if required commands exist
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi

# Step 1: Start Mock vLLM Server
echo -e "${YELLOW}Step 1: Starting Mock vLLM Server...${NC}"
if check_port 8001; then
    echo -e "${YELLOW}⚠️  Port 8001 already in use. Skipping vLLM server start.${NC}"
else
    # Create venv if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        pip install -q fastapi uvicorn pydantic
    else
        source venv/bin/activate
    fi

    # Start mock vLLM in background
    nohup python3 mock-vllm-server.py > logs/vllm.log 2>&1 &
    echo $! > .vllm.pid
    wait_for_service "http://localhost:8001/health" "Mock vLLM"
fi

# Step 2: Start Backend Server
echo -e "${YELLOW}Step 2: Starting Backend Server...${NC}"
if check_port 8000; then
    echo -e "${YELLOW}⚠️  Port 8000 already in use. Skipping backend start.${NC}"
else
    cd backend

    # Create venv if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        pip install -q -r requirements.txt
    else
        source venv/bin/activate
    fi

    # Copy env file if it doesn't exist
    if [ ! -f ".env" ]; then
        cp .env.example .env
    fi

    # Start backend in background
    mkdir -p ../logs
    nohup python3 run.py > ../logs/backend.log 2>&1 &
    echo $! > ../.backend.pid
    cd ..
    wait_for_service "http://localhost:8000/health" "Backend API"
fi

# Step 3: Start Frontend
echo -e "${YELLOW}Step 3: Starting Frontend...${NC}"
if check_port 5173; then
    echo -e "${YELLOW}⚠️  Port 5173 already in use. Skipping frontend start.${NC}"
else
    cd frontend

    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing dependencies..."
        npm install
    fi

    # Copy env file if it doesn't exist
    if [ ! -f ".env" ]; then
        cp .env.example .env
    fi

    # Start frontend in background
    mkdir -p ../logs
    nohup npm run dev > ../logs/frontend.log 2>&1 &
    echo $! > ../.frontend.pid
    cd ..
    sleep 3
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ All services started!${NC}"
echo "=========================================="
echo ""
echo "Services running at:"
echo "  🔹 Mock vLLM:  http://localhost:8001"
echo "  🔹 Backend:    http://localhost:8000"
echo "  🔹 Frontend:   http://localhost:5173"
echo ""
echo "📖 API Docs:    http://localhost:8000/docs"
echo ""
echo "Logs are saved in the 'logs/' directory"
echo ""
echo "To stop all services, run: ./stop-all.sh"
echo ""
echo -e "${GREEN}🎉 Open http://localhost:5173 in your browser!${NC}"
echo ""
