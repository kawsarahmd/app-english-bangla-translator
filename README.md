# English-Bangla Translator

A full-stack web application for bidirectional English-Bangla translation using a custom LLM deployed on vLLM.

## Features

### Frontend (React + TypeScript)
- Clean, responsive two-column translation interface
- Bidirectional translation (English ↔ Bangla)
- Real-time character count and translation time display
- Copy to clipboard functionality
- Translation history (last 10 translations)
- Language swap feature
- Error handling with user-friendly messages
- Health status indicator for backend and vLLM
- Mobile-friendly responsive design

### Backend (FastAPI + Python)
- RESTful API for translation services
- SQLite database for translation history
- vLLM integration for ML-powered translations
- Comprehensive monitoring and analytics endpoints
- Request validation and error handling
- CORS configuration for secure cross-origin requests
- Automatic database initialization

## Tech Stack

- **Frontend**: React, TypeScript, Vite, Axios
- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: SQLite
- **LLM Server**: vLLM
- **Architecture**: REST API

## Project Structure

```
app-english-bangla-translator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database configuration
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── routers/
│   │   │   └── translation.py   # API endpoints
│   │   └── services/
│   │       └── vllm_client.py   # vLLM client
│   ├── requirements.txt
│   ├── .env
│   └── run.py                   # Entry point
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── TranslationInterface.tsx
│   │   ├── services/
│   │   │   └── api.ts           # API client
│   │   ├── types/
│   │   │   └── index.ts         # TypeScript types
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn
- A running vLLM server with a translation model

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your vLLM server details
```

5. Run the backend:
```bash
python run.py
```

The backend will start on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env if needed (default: http://localhost:8000)
```

4. Run the frontend:
```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

## Configuration

### Backend Environment Variables (`.env`)

```bash
# vLLM Server Configuration
VLLM_HOST=localhost
VLLM_PORT=8001
VLLM_TIMEOUT=60

# Backend Configuration
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Database Configuration
DATABASE_URL=sqlite:///./translations.db

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# API Configuration
MAX_TEXT_LENGTH=5000
REQUEST_TIMEOUT=120
```

### Frontend Environment Variables (`.env`)

```bash
VITE_API_URL=http://localhost:8000
```

### vLLM Prompt Format

The vLLM client in `backend/app/services/vllm_client.py` uses a specific prompt format. You may need to adjust the `_format_prompt` method based on your translation model's training format:

```python
def _format_prompt(self, text: str, source_lang: str, target_lang: str) -> str:
    """Format the translation prompt for the model."""
    # Adjust this based on your model's expected format
    prompt = f"""Translate the following text from {source_name} to {target_name}.

{source_name}: {text}
{target_name}:"""
    return prompt
```

## API Endpoints

### Translation

**POST** `/translate`

Translate text between English and Bangla.

Request:
```json
{
  "text": "Hello, how are you?",
  "source_lang": "en",
  "target_lang": "bn"
}
```

Response:
```json
{
  "translated_text": "হ্যালো, আপনি কেমন আছেন?",
  "source_lang": "en",
  "target_lang": "bn",
  "processing_time": 245.67
}
```

### Health Check

**GET** `/health`

Check backend and vLLM server health.

Response:
```json
{
  "status": "healthy",
  "vllm_connected": true,
  "timestamp": "2024-01-15T12:00:00"
}
```

### Get Translations

**GET** `/translations?limit=100&offset=0&source_lang=en`

Get paginated list of translations with optional filtering.

Response:
```json
{
  "translations": [...],
  "total_count": 150,
  "limit": 100,
  "offset": 0
}
```

### Translation Statistics

**GET** `/translations/stats`

Get aggregated translation statistics.

Response:
```json
{
  "total_translations": 1000,
  "avg_processing_time": 234.56,
  "by_language_pair": {
    "en->bn": 600,
    "bn->en": 400
  },
  "errors_count": 10,
  "success_count": 990,
  "last_24h_count": 150
}
```

## Database Schema

### Translations Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| source_text | TEXT | Input text from user |
| translated_text | TEXT | Translated output |
| source_lang | VARCHAR(10) | Source language code ("en" or "bn") |
| target_lang | VARCHAR(10) | Target language code ("en" or "bn") |
| processing_time | FLOAT | Translation time in milliseconds |
| created_at | DATETIME | Timestamp of translation |
| user_ip | VARCHAR(50) | Client IP address (optional) |
| status | VARCHAR(20) | "success" or "error" |

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate
python run.py
```

The backend runs with hot-reload enabled in development mode.

### Frontend Development

```bash
cd frontend
npm run dev
```

The frontend uses Vite with hot module replacement (HMR).

### Building for Production

**Frontend**:
```bash
cd frontend
npm run build
```

The production build will be in `frontend/dist/`

**Backend**:

For production, disable reload and configure proper CORS:
```python
# In run.py
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8000,
    reload=False  # Disable in production
)
```

## Testing

### Test the Backend

1. Check API documentation: http://localhost:8000/docs
2. Test health endpoint:
```bash
curl http://localhost:8000/health
```

3. Test translation:
```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_lang": "en", "target_lang": "bn"}'
```

### Test the Frontend

1. Open http://localhost:5173
2. Enter text in the source panel
3. Click "Translate"
4. Verify translation appears in the target panel

## Deployment Considerations

1. **Backend**:
   - Use a production ASGI server (Gunicorn + Uvicorn workers)
   - Configure proper CORS origins for production domains
   - Set up logging and monitoring
   - Use environment variables for all configuration
   - Consider using PostgreSQL instead of SQLite for production

2. **Frontend**:
   - Build optimized production bundle
   - Serve static files via CDN or web server (Nginx, Apache)
   - Configure environment variables for production API URL
   - Enable HTTPS

3. **vLLM**:
   - Ensure vLLM server is accessible and properly configured
   - Set appropriate timeouts based on model size
   - Consider load balancing for high traffic

## Troubleshooting

### Backend Issues

**Database not initialized**:
- Delete `translations.db` and restart the server
- Database is automatically created on startup

**vLLM connection failed**:
- Check vLLM server is running
- Verify `VLLM_HOST` and `VLLM_PORT` in `.env`
- Test vLLM endpoint manually

**CORS errors**:
- Add your frontend URL to `CORS_ORIGINS` in `.env`
- Restart the backend server

### Frontend Issues

**API connection failed**:
- Check backend is running on correct port
- Verify `VITE_API_URL` in `.env`
- Check browser console for errors

**Build errors**:
- Delete `node_modules` and reinstall: `npm install`
- Clear cache: `npm cache clean --force`

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please open an issue on the GitHub repository.
