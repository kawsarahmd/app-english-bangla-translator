"""Translation API routes."""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Optional
import time
import logging

from ..database import get_db
from ..models import Translation
from ..schemas import (
    TranslationRequest,
    TranslationResponse,
    HealthResponse,
    TranslationListResponse,
    TranslationRecord,
    StatsResponse
)
from ..services.vllm_client import vllm_client

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/translate", response_model=TranslationResponse)
async def translate_text(
    request_data: TranslationRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Translate text from source language to target language.

    Args:
        request_data: Translation request with text and language codes
        request: FastAPI request object to get client IP
        db: Database session

    Returns:
        TranslationResponse with translated text and metadata
    """
    # Validate that source and target languages are different
    if request_data.source_lang == request_data.target_lang:
        raise HTTPException(
            status_code=400,
            detail="Source and target languages must be different"
        )

    # Get client IP
    client_ip = request.client.host if request.client else None

    # Start timing
    start_time = time.time()

    try:
        # Call vLLM service for translation
        translated_text = await vllm_client.translate(
            text=request_data.text,
            source_lang=request_data.source_lang,
            target_lang=request_data.target_lang
        )

        # Calculate processing time in milliseconds
        processing_time = (time.time() - start_time) * 1000

        # Save successful translation to database
        translation_record = Translation(
            source_text=request_data.text,
            translated_text=translated_text,
            source_lang=request_data.source_lang,
            target_lang=request_data.target_lang,
            processing_time=processing_time,
            user_ip=client_ip,
            status="success"
        )
        db.add(translation_record)
        db.commit()

        logger.info(
            f"Translation successful: {request_data.source_lang}->{request_data.target_lang}, "
            f"time={processing_time:.2f}ms"
        )

        return TranslationResponse(
            translated_text=translated_text,
            source_lang=request_data.source_lang,
            target_lang=request_data.target_lang,
            processing_time=processing_time
        )

    except Exception as e:
        # Calculate processing time even for errors
        processing_time = (time.time() - start_time) * 1000

        # Save failed translation to database
        translation_record = Translation(
            source_text=request_data.text,
            translated_text="",
            source_lang=request_data.source_lang,
            target_lang=request_data.target_lang,
            processing_time=processing_time,
            user_ip=client_ip,
            status="error"
        )
        db.add(translation_record)
        db.commit()

        logger.error(f"Translation failed: {str(e)}")

        raise HTTPException(
            status_code=503,
            detail=f"Translation service unavailable: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify backend and vLLM connection.

    Returns:
        HealthResponse with status and vLLM connection status
    """
    vllm_connected = await vllm_client.check_health()

    return HealthResponse(
        status="healthy" if vllm_connected else "degraded",
        vllm_connected=vllm_connected
    )


@router.get("/translations", response_model=TranslationListResponse)
async def get_translations(
    limit: int = 100,
    offset: int = 0,
    source_lang: Optional[str] = None,
    target_lang: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get paginated list of translations with optional filtering.

    Args:
        limit: Maximum number of translations to return (default 100)
        offset: Number of translations to skip (default 0)
        source_lang: Filter by source language (optional)
        target_lang: Filter by target language (optional)
        status: Filter by status (optional)
        db: Database session

    Returns:
        TranslationListResponse with list of translations and metadata
    """
    # Build query with filters
    query = db.query(Translation)

    if source_lang:
        query = query.filter(Translation.source_lang == source_lang)
    if target_lang:
        query = query.filter(Translation.target_lang == target_lang)
    if status:
        query = query.filter(Translation.status == status)

    # Get total count
    total_count = query.count()

    # Get paginated results
    translations = query.order_by(Translation.created_at.desc()).offset(offset).limit(limit).all()

    return TranslationListResponse(
        translations=[TranslationRecord.model_validate(t) for t in translations],
        total_count=total_count,
        limit=limit,
        offset=offset
    )


@router.get("/translations/stats", response_model=StatsResponse)
async def get_translation_stats(db: Session = Depends(get_db)):
    """
    Get translation statistics for monitoring and analytics.

    Args:
        db: Database session

    Returns:
        StatsResponse with aggregated statistics
    """
    # Total translations
    total_translations = db.query(func.count(Translation.id)).scalar() or 0

    # Average processing time (only for successful translations)
    avg_time = db.query(func.avg(Translation.processing_time)).filter(
        Translation.status == "success"
    ).scalar() or 0.0

    # Count by language pair
    language_pairs = db.query(
        Translation.source_lang,
        Translation.target_lang,
        func.count(Translation.id).label("count")
    ).group_by(Translation.source_lang, Translation.target_lang).all()

    by_language_pair = {
        f"{pair[0]}->{pair[1]}": pair[2] for pair in language_pairs
    }

    # Count by status
    success_count = db.query(func.count(Translation.id)).filter(
        Translation.status == "success"
    ).scalar() or 0

    errors_count = db.query(func.count(Translation.id)).filter(
        Translation.status == "error"
    ).scalar() or 0

    # Last 24 hours count
    yesterday = datetime.utcnow() - timedelta(days=1)
    last_24h_count = db.query(func.count(Translation.id)).filter(
        Translation.created_at >= yesterday
    ).scalar() or 0

    return StatsResponse(
        total_translations=total_translations,
        avg_processing_time=round(avg_time, 2),
        by_language_pair=by_language_pair,
        errors_count=errors_count,
        success_count=success_count,
        last_24h_count=last_24h_count
    )
