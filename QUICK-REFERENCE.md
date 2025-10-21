# ⚡ Quick Reference Card

## One-Command Startup

### Mac/Linux:
```bash
./start-all.sh
```

### Windows:
```bash
start-all.bat
```

---

## Manual Startup (3 Terminals)

### Terminal 1 - Mock vLLM:
```bash
cd app-english-bangla-translator
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fastapi uvicorn pydantic
python mock-vllm-server.py
```

### Terminal 2 - Backend:
```bash
cd app-english-bangla-translator/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Windows: copy
python run.py
```

### Terminal 3 - Frontend:
```bash
cd app-english-bangla-translator/frontend
npm install
cp .env.example .env  # Windows: copy
npm run dev
```

---

## Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | Main UI |
| Backend | http://localhost:8000 | API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Mock vLLM | http://localhost:8001 | Test server |
| Stats | http://localhost:8000/translations/stats | Analytics |

---

## Stop Services

### Automated:
```bash
./stop-all.sh
```

### Manual:
Press `CTRL + C` in each terminal

---

## Kill Stuck Ports

### Mac/Linux:
```bash
lsof -ti:8001 | xargs kill -9  # vLLM
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend
```

### Windows:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## Common Commands

### Backend:
```bash
# Run backend
cd backend && python run.py

# Check health
curl http://localhost:8000/health

# Test translation
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"hello","source_lang":"en","target_lang":"bn"}'
```

### Frontend:
```bash
# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## File Locations

### Configuration:
- Backend config: `backend/.env`
- Frontend config: `frontend/.env`

### Database:
- Location: `backend/translations.db`

### Logs:
- All logs: `logs/` folder

### Important Files:
- Mock server: `mock-vllm-server.py`
- Backend entry: `backend/run.py`
- Frontend entry: `frontend/src/main.tsx`

---

## Environment Variables

### Backend (.env):
```bash
VLLM_HOST=localhost
VLLM_PORT=8001
BACKEND_PORT=8000
DATABASE_URL=sqlite:///./translations.db
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend (.env):
```bash
VITE_API_URL=http://localhost:8000
```

---

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Port in use | Kill port (see above) |
| Module not found | Delete venv/node_modules, reinstall |
| Backend won't start | Check vLLM is running |
| Frontend won't connect | Check backend is running |
| Python not found | Try `python3` instead |

---

## Testing Checklist

- [ ] All 3 services running
- [ ] Green health banner appears
- [ ] Can translate "hello"
- [ ] Can swap languages
- [ ] Copy buttons work
- [ ] History shows up
- [ ] No errors in browser console

---

## Project URLs

- **Main app:** http://localhost:5173
- **API docs:** http://localhost:8000/docs
- **Health check:** http://localhost:8000/health
- **Translation stats:** http://localhost:8000/translations/stats
- **All translations:** http://localhost:8000/translations

---

## First Time Setup

1. Install: Python 3.8+, Node.js 18+
2. Run: `./start-all.sh` (or `.bat` on Windows)
3. Open: http://localhost:5173
4. Test: Translate "hello"

---

**For detailed instructions, see: INSTALLATION-GUIDE.md**
