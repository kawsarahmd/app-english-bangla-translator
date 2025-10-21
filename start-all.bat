@echo off
REM Automated startup script for Windows

echo ==========================================
echo Starting English-Bangla Translator
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

REM Create logs directory
if not exist "logs" mkdir logs

REM Step 1: Start Mock vLLM Server
echo Step 1: Starting Mock vLLM Server...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -q fastapi uvicorn pydantic
) else (
    call venv\Scripts\activate
)

start "Mock vLLM Server" /min cmd /c "python mock-vllm-server.py > logs\vllm.log 2>&1"
timeout /t 3 /nobreak >nul
echo Mock vLLM Server started on http://localhost:8001

REM Step 2: Start Backend Server
echo Step 2: Starting Backend Server...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -q -r requirements.txt
) else (
    call venv\Scripts\activate
)

if not exist ".env" copy .env.example .env

start "Backend Server" /min cmd /c "python run.py > ..\logs\backend.log 2>&1"
cd ..
timeout /t 5 /nobreak >nul
echo Backend Server started on http://localhost:8000

REM Step 3: Start Frontend
echo Step 3: Starting Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

if not exist ".env" copy .env.example .env

start "Frontend Server" /min cmd /c "npm run dev > ..\logs\frontend.log 2>&1"
cd ..
timeout /t 3 /nobreak >nul

echo.
echo ==========================================
echo All services started!
echo ==========================================
echo.
echo Services running at:
echo   Mock vLLM:  http://localhost:8001
echo   Backend:    http://localhost:8000
echo   Frontend:   http://localhost:5173
echo.
echo API Docs:    http://localhost:8000/docs
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:5173
echo.
echo Press any key to stop all services...
pause >nul

REM Stop services when user presses a key
taskkill /FI "WINDOWTITLE eq Mock vLLM Server*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Backend Server*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend Server*" /F >nul 2>&1

echo.
echo All services stopped.
pause
