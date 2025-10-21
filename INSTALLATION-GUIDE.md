# 📘 Complete Installation Guide - A to Z

This guide will walk you through every step needed to run the English-Bangla Translator on your laptop.

---

## 🎯 Overview

You'll need to run **3 services**:
1. **Mock vLLM Server** (simulates translation model) - Port 8001
2. **Backend API** (FastAPI) - Port 8000
3. **Frontend** (React) - Port 5173

---

## ✅ Prerequisites Installation

### Step 1: Check what you already have

Open Terminal (Mac/Linux) or Command Prompt (Windows) and run:

```bash
python --version    # Need: 3.8 or higher
node --version      # Need: 18 or higher
npm --version       # Should come with Node.js
git --version       # For version control
```

### Step 2: Install missing software

#### 🪟 **Windows Users:**

1. **Install Python:**
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.11.x"
   - Run the installer
   - ⚠️ **IMPORTANT:** Check ☑️ "Add Python to PATH" before clicking Install
   - Verify: Open new Command Prompt → `python --version`

2. **Install Node.js:**
   - Go to: https://nodejs.org/
   - Download "LTS" version (recommended)
   - Run the installer with default settings
   - Verify: Open new Command Prompt → `node --version`

3. **Install Git (optional but recommended):**
   - Go to: https://git-scm.com/download/win
   - Download and install with default settings

#### 🍎 **Mac Users:**

Option 1 - Using Homebrew (recommended):
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Node.js
brew install python@3.11 node
```

Option 2 - Manual installation:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/

#### 🐧 **Linux Users (Ubuntu/Debian):**

```bash
# Update package list
sudo apt update

# Install Python
sudo apt install python3.11 python3-pip python3-venv

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Git (usually pre-installed)
sudo apt install git
```

---

## 📥 Get the Project Files

### If you have Git:
```bash
# Clone the repository
git clone <your-repository-url>
cd app-english-bangla-translator
```

### If you don't have Git:
1. Download the ZIP file from GitHub
2. Extract it to a folder (e.g., `Documents/app-english-bangla-translator`)
3. Open Terminal/Command Prompt and navigate to that folder:
   ```bash
   cd path/to/app-english-bangla-translator
   ```

---

## 🚀 Method 1: Automated Startup (Easiest)

### For Mac/Linux:

```bash
# Make scripts executable (first time only)
chmod +x start-all.sh stop-all.sh

# Start everything
./start-all.sh

# When done, stop everything
./stop-all.sh
```

### For Windows:

```bash
# Just double-click the file:
start-all.bat

# Or run from Command Prompt:
start-all.bat
```

The automated script will:
- ✅ Create virtual environments
- ✅ Install all dependencies
- ✅ Start all 3 services
- ✅ Open your browser automatically

**Then go to:** http://localhost:5173

---

## 🔧 Method 2: Manual Startup (Recommended for learning)

If you want to understand what's happening, follow these manual steps.

### Terminal/Window 1: Start Mock vLLM Server

```bash
# Navigate to project root
cd app-english-bangla-translator

# Create virtual environment
python -m venv venv
# Or on some systems:
python3 -m venv venv

# Activate virtual environment:
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Your prompt should now show (venv)

# Install required packages
pip install fastapi uvicorn pydantic

# Run the mock vLLM server
python mock-vllm-server.py
```

✅ **Success looks like:**
```
🚀 Starting Mock vLLM Server
⚠️  WARNING: This is a MOCK server for testing only!
Server will run on: http://localhost:8001
INFO:     Uvicorn running on http://0.0.0.0:8001
```

**Keep this window open and running!**

---

### Terminal/Window 2: Start Backend Server

Open a **NEW** terminal/command prompt window:

```bash
# Navigate to backend folder
cd app-english-bangla-translator/backend

# Create virtual environment
python -m venv venv

# Activate it:
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (first time only)
# Mac/Linux:
cp .env.example .env
# Windows:
copy .env.example .env

# Run the backend
python run.py
```

✅ **Success looks like:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
```

**Keep this window open and running!**

---

### Terminal/Window 3: Start Frontend

Open **another NEW** terminal/command prompt window:

```bash
# Navigate to frontend folder
cd app-english-bangla-translator/frontend

# Install dependencies (first time only, takes a few minutes)
npm install

# Create .env file (first time only)
# Mac/Linux:
cp .env.example .env
# Windows:
copy .env.example .env

# Start the development server
npm run dev
```

✅ **Success looks like:**
```
  VITE v5.0.12  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Keep this window open and running!**

---

## 🌐 Open the Application

Open your web browser and go to:

```
http://localhost:5173
```

You should see the **English-Bangla Translator** interface!

---

## ✨ Test the Application

1. **Check Health Status:**
   - You should see a green banner saying "Backend: ✓ Connected | vLLM: ✓ Connected"

2. **Try a Translation:**
   - Select "English" → "বাংলা (Bangla)"
   - Type: `hello`
   - Click "Translate"
   - You should see: `[MOCK BN] hello` or `হ্যালো`

3. **Try Reverse Translation:**
   - Click the swap button (⇄)
   - Type some Bangla text
   - Click "Translate"

4. **Check Other Features:**
   - Copy buttons work
   - Character counter updates
   - Translation history appears below
   - Processing time is displayed

---

## 🔍 Verify Everything is Working

### Check each service:

1. **Mock vLLM:** http://localhost:8001
   - Should show: "Mock vLLM Server for Testing"

2. **Backend API:** http://localhost:8000
   - Should show: API information

3. **API Documentation:** http://localhost:8000/docs
   - Interactive API documentation (Swagger UI)

4. **Frontend:** http://localhost:5173
   - Translation interface

---

## 🛑 How to Stop Everything

### Method 1: Using stop script

Mac/Linux:
```bash
./stop-all.sh
```

Windows:
```bash
# Just press any key in the start-all.bat window
```

### Method 2: Manual stop

In each terminal window, press: **CTRL + C**

---

## 🐛 Troubleshooting

### Problem: "Port already in use"

**Solution:** Kill the process using that port

**Mac/Linux:**
```bash
# Kill port 8001 (vLLM)
lsof -ti:8001 | xargs kill -9

# Kill port 8000 (Backend)
lsof -ti:8000 | xargs kill -9

# Kill port 5173 (Frontend)
lsof -ti:5173 | xargs kill -9
```

**Windows:**
```bash
# Find process on port 8000 (example)
netstat -ano | findstr :8000

# Kill it (replace PID with the number from above)
taskkill /PID <PID> /F
```

---

### Problem: "python: command not found"

**Solution:** Try `python3` instead of `python`:
```bash
python3 --version
python3 -m venv venv
```

Or add Python to your PATH (see installation section).

---

### Problem: "npm: command not found"

**Solution:** Node.js not installed or not in PATH
- Reinstall Node.js and restart terminal
- Check: `node --version` should also work

---

### Problem: Backend shows "vLLM connection failed"

**Solutions:**
1. Make sure mock vLLM server is running (Terminal 1)
2. Check `backend/.env` file:
   ```
   VLLM_HOST=localhost
   VLLM_PORT=8001
   ```
3. Test vLLM manually: http://localhost:8001/health

---

### Problem: Frontend shows "Unable to connect"

**Solutions:**
1. Make sure backend is running (Terminal 2)
2. Check `frontend/.env` file:
   ```
   VITE_API_URL=http://localhost:8000
   ```
3. Test backend manually: http://localhost:8000/health

---

### Problem: "Module not found" errors

**Solution:** Reinstall dependencies

**Backend:**
```bash
cd backend
rm -rf venv  # Delete old virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules  # Delete old modules
npm install
```

---

## 📊 Project Structure

```
app-english-bangla-translator/
├── mock-vllm-server.py      ← Mock translation server
├── start-all.sh             ← Auto-start script (Mac/Linux)
├── start-all.bat            ← Auto-start script (Windows)
├── stop-all.sh              ← Auto-stop script
├── backend/
│   ├── app/                 ← Backend code
│   ├── requirements.txt     ← Python dependencies
│   ├── .env                 ← Backend configuration
│   └── run.py              ← Backend entry point
├── frontend/
│   ├── src/                ← Frontend code
│   ├── package.json        ← Node dependencies
│   └── .env                ← Frontend configuration
└── README.md               ← Full documentation
```

---

## 🎓 Next Steps

### For Development:
1. Modify UI: Edit `frontend/src/App.css`
2. Add features: Check `backend/app/routers/translation.py`
3. View logs: Check `logs/` folder
4. Database: `backend/translations.db` (SQLite)

### For Production:
1. Replace mock vLLM with real translation model
2. Update prompt format in `backend/app/services/vllm_client.py`
3. Build frontend: `npm run build`
4. Deploy with Docker or cloud service

---

## 📚 Additional Resources

- **API Documentation:** http://localhost:8000/docs (when backend is running)
- **Full README:** See `README.md` in project root
- **Quick Start:** See `START-HERE.md`
- **Translation Stats:** http://localhost:8000/translations/stats

---

## 💡 Tips

1. **First time setup takes longer** (installing dependencies)
2. **Next times are faster** (just run the start scripts)
3. **Keep all 3 terminals running** while using the app
4. **Check the health banner** at the top of the webpage
5. **Mock server is for testing only** - set up real vLLM for production

---

## ✅ You're all set!

If you followed these steps, you should now have a working translation application running locally on your laptop!

**Open:** http://localhost:5173 and start translating! 🎉

---

**Need more help?** Check the troubleshooting section or refer to the detailed README.md file.
