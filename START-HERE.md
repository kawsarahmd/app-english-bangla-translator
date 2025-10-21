# 🚀 Quick Start Guide - Run Locally in 3 Steps

Follow these steps to run the English-Bangla Translator on your laptop.

## Step 1: Install Prerequisites

### Check what you have:
```bash
python --version   # Need 3.8+
node --version     # Need 18+
npm --version
```

### If missing, install:

**Windows:**
- Python: https://www.python.org/downloads/ (Check "Add to PATH")
- Node.js: https://nodejs.org/

**Mac:**
```bash
brew install python@3.11 node
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.11 python3-pip python3-venv nodejs npm
```

---

## Step 2: Start Mock vLLM Server (For Testing)

**Terminal 1 - Start Mock vLLM:**

```bash
# Navigate to project folder
cd app-english-bangla-translator

# Create Python virtual environment
python -m venv venv

# Activate it:
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn pydantic

# Run mock vLLM server
python mock-vllm-server.py
```

✅ You should see: "Mock vLLM Server running on http://localhost:8001"

**Keep this terminal running!**

---

## Step 3: Start Backend Server

**Terminal 2 - Start Backend:**

```bash
# Navigate to backend folder
cd app-english-bangla-translator/backend

# Create virtual environment
python -m venv venv

# Activate it:
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run backend server
python run.py
```

✅ You should see: "Uvicorn running on http://0.0.0.0:8000"

**Keep this terminal running!**

---

## Step 4: Start Frontend

**Terminal 3 - Start Frontend:**

```bash
# Navigate to frontend folder
cd app-english-bangla-translator/frontend

# Install dependencies (first time only)
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

✅ You should see: "Local: http://localhost:5173"

**Keep this terminal running!**

---

## Step 5: Open in Browser

Open your browser and go to:
```
http://localhost:5173
```

You should see the translation interface!

---

## Test the Application

1. Select languages (e.g., English → Bangla)
2. Type "hello" in the left text box
3. Click "Translate"
4. You should see "[MOCK BN] hello" or "হ্যালো" in the right box

**Note:** The mock server provides fake translations for testing. For real translations, you need to set up a real vLLM server with a translation model.

---

## Troubleshooting

### Port already in use?

**Backend (port 8000):**
```bash
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Frontend (port 5173):**
```bash
# Mac/Linux:
lsof -ti:5173 | xargs kill -9

# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

**Mock vLLM (port 8001):**
```bash
# Mac/Linux:
lsof -ti:8001 | xargs kill -9

# Windows:
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

### Backend connection error?

- Make sure mock vLLM server is running on port 8001
- Check `backend/.env` file has: `VLLM_HOST=localhost` and `VLLM_PORT=8001`

### Frontend can't connect?

- Make sure backend is running on port 8000
- Check `frontend/.env` file has: `VITE_API_URL=http://localhost:8000`

---

## Using a Real Translation Model

To use a real translation model instead of the mock server:

1. **Stop the mock server**
2. **Install vLLM:**
   ```bash
   pip install vllm
   ```

3. **Download a translation model from HuggingFace:**
   - Example: `facebook/nllb-200-distilled-600M`

4. **Start vLLM with your model:**
   ```bash
   python -m vllm.entrypoints.openai.api_server \
     --model facebook/nllb-200-distilled-600M \
     --port 8001
   ```

5. **Update the prompt format** in `backend/app/services/vllm_client.py` to match your model's expected format

---

## Summary of Running Services

When everything is running, you should have:

| Service | URL | Terminal |
|---------|-----|----------|
| Mock vLLM | http://localhost:8001 | Terminal 1 |
| Backend API | http://localhost:8000 | Terminal 2 |
| Frontend UI | http://localhost:5173 | Terminal 3 |

**API Documentation:** http://localhost:8000/docs

---

## Next Steps

- Check API docs: http://localhost:8000/docs
- View translation stats: http://localhost:8000/translations/stats
- Configure real vLLM model for production use
- Customize the UI in `frontend/src/App.css`

---

Need help? Check the main README.md or open an issue on GitHub.
