#!/bin/bash

# Script to stop all running services

echo "=========================================="
echo "🛑 Stopping all services..."
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Function to stop a service
stop_service() {
    local pid_file=$1
    local name=$2

    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid 2>/dev/null
            echo -e "${GREEN}✓${NC} Stopped $name (PID: $pid)"
        else
            echo -e "${RED}⚠${NC}  $name was not running"
        fi
        rm "$pid_file"
    else
        echo -e "${RED}⚠${NC}  No PID file found for $name"
    fi
}

# Stop all services
stop_service ".frontend.pid" "Frontend"
stop_service ".backend.pid" "Backend"
stop_service ".vllm.pid" "Mock vLLM"

# Also kill by port in case PID files are missing
echo ""
echo "Cleaning up ports..."

# Function to kill process on port
kill_port() {
    local port=$1
    local name=$2

    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        lsof -ti:$port | xargs kill -9 2>/dev/null
        echo -e "${GREEN}✓${NC} Cleaned up port $port ($name)"
    fi
}

kill_port 5173 "Frontend"
kill_port 8000 "Backend"
kill_port 8001 "vLLM"

echo ""
echo "=========================================="
echo -e "${GREEN}✅ All services stopped${NC}"
echo "=========================================="
echo ""
