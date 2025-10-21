"""SQLAlchemy models for the database."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from .database import Base


class Translation(Base):
    """Translation model to store translation history."""

    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_lang = Column(String(10), nullable=False, index=True)
    target_lang = Column(String(10), nullable=False, index=True)
    processing_time = Column(Float, nullable=False)  # in milliseconds
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    user_ip = Column(String(50), nullable=True)
    status = Column(String(20), default="success", nullable=False, index=True)

    def __repr__(self):
        return f"<Translation(id={self.id}, {self.source_lang}->{self.target_lang}, status={self.status})>"
