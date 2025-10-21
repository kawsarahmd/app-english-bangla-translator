"""vLLM client for translation service."""
import httpx
import os
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class VLLMClient:
    """Client for communicating with vLLM server."""

    def __init__(self):
        self.host = os.getenv("VLLM_HOST", "localhost")
        self.port = int(os.getenv("VLLM_PORT", "8001"))
        self.timeout = int(os.getenv("VLLM_TIMEOUT", "60"))
        self.base_url = f"http://{self.host}:{self.port}"
        self.client = httpx.AsyncClient(timeout=self.timeout)

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text using vLLM server.

        Args:
            text: Text to translate
            source_lang: Source language code (en or bn)
            target_lang: Target language code (en or bn)

        Returns:
            Translated text

        Raises:
            httpx.HTTPError: If vLLM server is unreachable or returns an error
        """
        # Format the prompt for the translation model
        # Adjust this based on your specific model's expected format
        prompt = self._format_prompt(text, source_lang, target_lang)

        try:
            # vLLM typically exposes /v1/completions or /generate endpoint
            # Adjust the endpoint and payload based on your vLLM setup
            response = await self.client.post(
                f"{self.base_url}/v1/completions",
                json={
                    "prompt": prompt,
                    "max_tokens": 2048,
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "stop": ["\n\n", "###"],  # Adjust based on your model
                }
            )
            response.raise_for_status()

            result = response.json()
            # Extract translated text from response
            # Adjust based on your vLLM response format
            translated_text = result.get("choices", [{}])[0].get("text", "").strip()

            if not translated_text:
                raise ValueError("Empty translation received from vLLM")

            return translated_text

        except httpx.HTTPError as e:
            logger.error(f"vLLM request failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during translation: {str(e)}")
            raise

    def _format_prompt(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Format the translation prompt for the model.

        Adjust this method based on your specific model's training format.
        """
        lang_names = {
            "en": "English",
            "bn": "Bangla"
        }

        source_name = lang_names.get(source_lang, source_lang)
        target_name = lang_names.get(target_lang, target_lang)

        # Example prompt format - adjust based on your model
        prompt = f"""Translate the following text from {source_name} to {target_name}.

{source_name}: {text}
{target_name}:"""

        return prompt

    async def check_health(self) -> bool:
        """
        Check if vLLM server is reachable and healthy.

        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/health",
                timeout=5.0
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"vLLM health check failed: {str(e)}")
            return False

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Global vLLM client instance
vllm_client = VLLMClient()
