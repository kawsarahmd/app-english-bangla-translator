"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from datetime import datetime


class TranslationRequest(BaseModel):
    """Request schema for translation."""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to translate")
    source_lang: str = Field(..., pattern="^(en|bn)$", description="Source language code")
    target_lang: str = Field(..., pattern="^(en|bn)$", description="Target language code")

    @field_validator('text')
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Text cannot be empty or only whitespace')
        return v.strip()

    @field_validator('source_lang', 'target_lang')
    @classmethod
    def validate_lang_codes(cls, v: str) -> str:
        if v not in ['en', 'bn']:
            raise ValueError('Language code must be either "en" or "bn"')
        return v


class TranslationResponse(BaseModel):
    """Response schema for translation."""
    translated_text: str
    source_lang: str
    target_lang: str
    processing_time: float  # in milliseconds

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Response schema for health check."""
    status: str
    vllm_connected: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TranslationRecord(BaseModel):
    """Schema for translation record from database."""
    id: int
    source_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    processing_time: float
    created_at: datetime
    user_ip: Optional[str] = None
    status: str

    class Config:
        from_attributes = True


class TranslationListResponse(BaseModel):
    """Response schema for list of translations."""
    translations: List[TranslationRecord]
    total_count: int
    limit: int
    offset: int


class StatsResponse(BaseModel):
    """Response schema for translation statistics."""
    total_translations: int
    avg_processing_time: float
    by_language_pair: Dict[str, int]
    errors_count: int
    success_count: int
    last_24h_count: int
