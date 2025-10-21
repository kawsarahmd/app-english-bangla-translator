"""
Mock vLLM Server for Testing
This is a simple mock server that simulates vLLM responses for testing purposes.
Use this ONLY for testing the application without a real translation model.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing import List, Optional

app = FastAPI(title="Mock vLLM Server")


class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    stop: Optional[List[str]] = None


class CompletionChoice(BaseModel):
    text: str
    index: int
    finish_reason: str


class CompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[CompletionChoice]


# Simple mock translations for testing
MOCK_TRANSLATIONS = {
    "hello": "হ্যালো",
    "how are you": "আপনি কেমন আছেন",
    "thank you": "ধন্যবাদ",
    "good morning": "সুপ্রভাত",
    "goodbye": "বিদায়",
}


def mock_translate(text: str, source_lang: str, target_lang: str) -> str:
    """Generate a mock translation."""
    text_lower = text.lower().strip()

    # Check if we have a mock translation
    if target_lang == "bn":  # English to Bangla
        return MOCK_TRANSLATIONS.get(text_lower, f"[MOCK BN] {text}")
    else:  # Bangla to English
        return f"[MOCK EN] {text}"


@app.post("/v1/completions")
async def create_completion(request: CompletionRequest):
    """Mock completion endpoint that simulates vLLM."""
    prompt = request.prompt

    # Extract translation info from prompt
    # Expected format: "Translate ... English: <text>\nBangla:"
    lines = prompt.split("\n")
    text_to_translate = ""
    source_lang = "en"
    target_lang = "bn"

    for line in lines:
        if "English:" in line or "Bangla:" in line:
            parts = line.split(":", 1)
            if len(parts) == 2:
                text_to_translate = parts[1].strip()
                if "English:" in line:
                    source_lang = "en"
                    target_lang = "bn"
                else:
                    source_lang = "bn"
                    target_lang = "en"

    # Generate mock translation
    translated_text = mock_translate(text_to_translate, source_lang, target_lang)

    return CompletionResponse(
        id="mock-completion-id",
        object="text_completion",
        created=1234567890,
        model="mock-translation-model",
        choices=[
            CompletionChoice(
                text=translated_text,
                index=0,
                finish_reason="stop"
            )
        ]
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Mock vLLM Server for Testing",
        "note": "This is NOT a real translation model. Use for testing only.",
        "endpoints": {
            "completions": "/v1/completions",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Starting Mock vLLM Server")
    print("=" * 50)
    print("\n⚠️  WARNING: This is a MOCK server for testing only!")
    print("It does NOT perform real translations.")
    print("For production, use a real vLLM server with a translation model.\n")
    print("Server will run on: http://localhost:8001")
    print("=" * 50)

    uvicorn.run(app, host="0.0.0.0", port=8001)
