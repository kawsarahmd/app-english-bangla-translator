# 🎯 How to Run Locally - Simple Visual Guide

## 📋 What You Need (5 minutes)

| Software | Minimum Version | Check Command | Download Link |
|----------|----------------|---------------|---------------|
| Python | 3.8+ | `python --version` | https://python.org/downloads |
| Node.js | 18+ | `node --version` | https://nodejs.org |
| npm | 8+ | `npm --version` | Comes with Node.js |

---

## 🚀 Easiest Way: One Command (Recommended)

### Step 1: Open Terminal

**Windows:** Press `Win + R`, type `cmd`, press Enter
**Mac:** Press `Cmd + Space`, type `Terminal`, press Enter
**Linux:** Press `Ctrl + Alt + T`

### Step 2: Navigate to Project

```bash
cd path/to/app-english-bangla-translator
```

### Step 3: Run Start Script

**Mac/Linux:**
```bash
chmod +x start-all.sh   # First time only
./start-all.sh
```

**Windows:**
```bash
start-all.bat
```

### Step 4: Open Browser

The script will automatically open http://localhost:5173

**That's it! You're done! 🎉**

---

## 🔧 Alternative: Manual Method (3 Terminals)

If the automated script doesn't work, follow this manual process:

### Visual Layout:

```
┌─────────────────┬─────────────────┬─────────────────┐
│   Terminal 1    │   Terminal 2    │   Terminal 3    │
│   Mock vLLM     │    Backend      │    Frontend     │
│   Port 8001     │   Port 8000     │   Port 5173     │
└─────────────────┴─────────────────┴─────────────────┘
```

### Terminal 1: Mock vLLM Server

```bash
# Navigate to project root
cd app-english-bangla-translator

# Create and activate virtual environment
python -m venv venv

# Activate (choose your OS):
source venv/bin/activate              # Mac/Linux
venv\Scripts\activate                 # Windows

# Install dependencies
pip install fastapi uvicorn pydantic

# Start mock server
python mock-vllm-server.py
```

**✅ You should see:**
```
🚀 Starting Mock vLLM Server
Server will run on: http://localhost:8001
INFO:     Uvicorn running on http://0.0.0.0:8001
```

**LEAVE THIS RUNNING** ⚠️

---

### Terminal 2: Backend Server

Open a **NEW** terminal window:

```bash
# Navigate to backend
cd app-english-bangla-translator/backend

# Create and activate virtual environment
python -m venv venv

# Activate (choose your OS):
source venv/bin/activate              # Mac/Linux
venv\Scripts\activate                 # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment file (first time only)
cp .env.example .env                  # Mac/Linux
copy .env.example .env                # Windows

# Start backend
python run.py
```

**✅ You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**LEAVE THIS RUNNING** ⚠️

---

### Terminal 3: Frontend

Open **ANOTHER NEW** terminal window:

```bash
# Navigate to frontend
cd app-english-bangla-translator/frontend

# Install dependencies (first time only - takes ~2 minutes)
npm install

# Setup environment file (first time only)
cp .env.example .env                  # Mac/Linux
copy .env.example .env                # Windows

# Start frontend
npm run dev
```

**✅ You should see:**
```
  VITE v5.0.12  ready in 500 ms

  ➜  Local:   http://localhost:5173/
```

**LEAVE THIS RUNNING** ⚠️

---

## 🌐 Access the Application

Open your browser and go to:

### 🎨 Main Application
```
http://localhost:5173
```

### 📚 Other URLs

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Backend API |
| http://localhost:8000/docs | Interactive API Documentation |
| http://localhost:8000/health | Health Check |
| http://localhost:8000/translations/stats | View Statistics |
| http://localhost:8001 | Mock vLLM Server |

---

## ✨ Test It Works

### 1. Check Health Status
Look at the top of the page. You should see a **green banner**:
```
Backend: ✓ Connected | vLLM: ✓ Connected
```

### 2. Try Translation

**Simple Test:**
1. Select: **English** → **বাংলা (Bangla)**
2. Type in left box: `hello`
3. Click **Translate** button
4. Right box shows: `[MOCK BN] hello` or `হ্যালো`

**Advanced Test:**
1. Try: `how are you`
2. Expected: `[MOCK BN] how are you` or `আপনি কেমন আছেন`
3. Click the **⇄** button to swap languages
4. Try translating back

### 3. Test Features

- ✅ Click **Copy** buttons
- ✅ Check character counter (bottom of left box)
- ✅ See translation time (appears after translating)
- ✅ View history (appears below after multiple translations)
- ✅ Try **Clear** button

---

## 🛑 How to Stop

### If using automated script:
```bash
./stop-all.sh          # Mac/Linux
# Or press any key in start-all.bat window (Windows)
```

### If using manual method:
In each of the 3 terminal windows, press:
```
Ctrl + C
```

---

## 🐛 Common Problems & Quick Fixes

### Problem 1: "Port already in use"

**Error message:**
```
Error: Address already in use
```

**Fix for Mac/Linux:**
```bash
# Kill port 8001 (vLLM)
lsof -ti:8001 | xargs kill -9

# Kill port 8000 (Backend)
lsof -ti:8000 | xargs kill -9

# Kill port 5173 (Frontend)
lsof -ti:5173 | xargs kill -9
```

**Fix for Windows:**
```bash
# Find what's using port 8000 (example)
netstat -ano | findstr :8000

# Note the PID number, then:
taskkill /PID <number> /F
```

---

### Problem 2: "python: command not found"

**Fix:**
Try using `python3` instead:
```bash
python3 --version
python3 -m venv venv
python3 mock-vllm-server.py
```

---

### Problem 3: Backend shows red "Disconnected"

**Cause:** Mock vLLM server isn't running

**Fix:**
1. Check Terminal 1 is still running mock server
2. Visit http://localhost:8001 - should show a message
3. Restart mock server if needed

---

### Problem 4: Frontend won't load

**Cause:** Backend isn't running

**Fix:**
1. Check Terminal 2 is still running backend
2. Visit http://localhost:8000 - should show API info
3. Restart backend if needed

---

### Problem 5: "npm: command not found"

**Cause:** Node.js not installed

**Fix:**
1. Install Node.js from https://nodejs.org
2. Close and reopen terminal
3. Test: `node --version`

---

## 📁 Project Structure

```
app-english-bangla-translator/
│
├── 📄 HOW-TO-RUN.md (this file)        ← You are here
├── 📄 START-HERE.md                     ← Quick 3-step guide
├── 📄 INSTALLATION-GUIDE.md             ← Detailed guide
├── 📄 QUICK-REFERENCE.md                ← Command cheat sheet
├── 📄 README.md                         ← Full documentation
│
├── 🐍 mock-vllm-server.py              ← Test server
├── 🚀 start-all.sh                     ← Auto-start (Mac/Linux)
├── 🚀 start-all.bat                    ← Auto-start (Windows)
├── 🛑 stop-all.sh                      ← Stop all services
│
├── backend/
│   ├── app/                            ← Backend code
│   ├── requirements.txt                ← Python packages
│   ├── .env                            ← Configuration
│   └── run.py                          ← Start backend
│
└── frontend/
    ├── src/                            ← Frontend code
    ├── package.json                    ← Node packages
    ├── .env                            ← Configuration
    └── index.html                      ← Entry point
```

---

## 📚 Which Guide Should I Read?

| Your Situation | Read This |
|----------------|-----------|
| Just want to run it quickly | **START-HERE.md** (you are here) |
| First time setup | **INSTALLATION-GUIDE.md** |
| Need command reference | **QUICK-REFERENCE.md** |
| Want full documentation | **README.md** |
| Developing/customizing | **README.md** |

---

## ⏱️ Time Estimates

| Task | First Time | Next Times |
|------|-----------|------------|
| Install prerequisites | 10-15 min | Already done |
| Download project | 1 min | Already done |
| Install dependencies | 5-10 min | 30 sec |
| Start all services | 2 min | 30 sec |
| **Total** | **~20 min** | **~1 min** |

---

## 🎯 Success Checklist

Before you start translating, make sure:

- [ ] All 3 terminal windows are open and running
- [ ] No error messages in any terminal
- [ ] Green health banner appears on webpage
- [ ] Can access http://localhost:5173
- [ ] Test translation works (try "hello")

If all checked, **you're ready to use the app!** 🎉

---

## 🆘 Still Having Issues?

1. **Read the detailed guide:** `INSTALLATION-GUIDE.md`
2. **Check your terminal output** for specific error messages
3. **Try the troubleshooting section** in README.md
4. **Restart everything:**
   - Close all terminals
   - Follow the manual method step by step
   - Check each step for errors

---

## 💡 Pro Tips

1. **Bookmark these URLs:**
   - App: http://localhost:5173
   - Docs: http://localhost:8000/docs

2. **Use the automated scripts** to save time

3. **Keep terminals visible** so you can see if any crash

4. **First run takes longer** (installing packages)

5. **Next runs are much faster** (packages already installed)

---

## 🎓 Next Steps After Getting It Running

1. **Explore the UI** - Try all features
2. **Check API docs** - http://localhost:8000/docs
3. **View statistics** - http://localhost:8000/translations/stats
4. **Read the code** - Start with `frontend/src/App.tsx`
5. **Customize styling** - Edit `frontend/src/App.css`

---

## ✅ You're All Set!

**Quick command to start everything:**

Mac/Linux: `./start-all.sh`
Windows: `start-all.bat`

**Then open:** http://localhost:5173

**Happy translating! 🌐✨**
