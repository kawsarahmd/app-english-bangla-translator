"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv

from .database import init_db
from .routers import translation

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="English-Bangla Translation API",
    description="API for bidirectional English-Bangla translation using vLLM",
    version="1.0.0"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(translation.router, tags=["translation"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")
    logger.info(f"CORS enabled for origins: {cors_origins}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down...")
    from .services.vllm_client import vllm_client
    await vllm_client.close()
    logger.info("Shutdown complete")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "English-Bangla Translation API",
        "version": "1.0.0",
        "endpoints": {
            "translate": "/translate",
            "health": "/health",
            "translations": "/translations",
            "stats": "/translations/stats",
            "docs": "/docs"
        }
    }
