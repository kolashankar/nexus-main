"""AI Client for LLM interactions"""

import os
import json
from typing import Any, Dict, List, Optional
import logging

try:
    from google import genai
    from google.genai.errors import APIError
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    # Note: google-generativeai is in requirements.txt, so this should not happen
    logging.warning(
        "google-generativeai not available. AI features will be limited.")

logger = logging.getLogger(__name__)


class AIClient:
    """Unified AI client for all LLM interactions"""

    def __init__(self):
        # Change to GEMINI_API_KEY (or GOOGLE_API_KEY which is often used)
        self.api_key = os.getenv("GEMINI_API_KEY") # Use GEMINI_API_KEY
        self.client: Optional[genai.Client] = None

        if GEMINI_AVAILABLE and self.api_key:
            try:
                # Initialize Gemini Client
                # The google-generativeai library automatically uses the
                # GOOGLE_API_KEY environment variable. We set it if we read it
                # from a custom name, or let the library handle GOOGLE_API_KEY.
                # If we rely on os.getenv("GEMINI_API_KEY"), we must pass it explicitly
                # or set GOOGLE_API_KEY for the client to find it.
                os.environ["GOOGLE_API_KEY"] = self.api_key
                self.client = genai.Client()
                logger.info("AI Client initialized successfully using Gemini")
            except Exception as e:
                logger.error(f"Failed to initialize AI client: {e}")
                self.client = None
                
    # Helper to convert messages format (assuming a 'role' and 'content' dict list)
    def _convert_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Converts internal message format to Gemini's expected 'contents' structure."""
        converted = []
        for message in messages:
            # Gemini typically uses 'user' and 'model' as roles in the history,
            # and 'user' for the last prompt.
            role = message.get("role", "user")
            # Map 'system' or other internal roles to 'user' for Gemini's single-turn/user-centric model
            if role not in ["user", "model"]:
                role = "user"
            
            # Simple message history for now, assuming the provided format is simple
            # If the backend is using tool calls/structured output, this needs further refinement
            converted.append({
                "role": role, 
                "parts": [{"text": message.get("content", "")}]
            })
        return converted

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gemini-2.5-flash", # Changed default model
        temperature: float = 0.7,
        response_format: Optional[Dict[str, str]] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get chat completion from LLM"""

        if not self.client:
            logger.warning("AI client not available, returning mock response")
            return self._mock_response(messages)

        try:
            # Convert messages to Gemini format
            gemini_messages = self._convert_messages(messages)
            
            # Gemini API parameters
            config_kwargs = {}
            if temperature is not None:
                config_kwargs["temperature"] = temperature
            if max_tokens is not None:
                config_kwargs["max_output_tokens"] = max_tokens
            
            # response_format in the old system likely means JSON mode.
            if response_format and response_format.get("type") == "json_object":
                config_kwargs["response_mime_type"] = "application/json"
                # Add a system instruction if possible to guide the JSON output
                # NOTE: System instructions are better placed in the initial messages list.
                
            config = genai.types.GenerateContentConfig(**config_kwargs) if config_kwargs else None


            # Call the Gemini API
            response = await self.client.models.generate_content(
                model=model,
                contents=gemini_messages,
                config=config,
            )

            # Extract content and usage
            return {
                "content": response.text,
                "model": model, # Model used
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count,
                    "completion_tokens": response.usage_metadata.candidates_token_count,
                    "total_tokens": response.usage_metadata.total_token_count
                }
            }
        except APIError as e:
            logger.error(f"Gemini API error: {e}")
            return self._mock_response(messages)
        except Exception as e:
            logger.error(f"AI chat completion error: {e}")
            return self._mock_response(messages)

    def _mock_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Mock response when AI is not available"""
        # Ensure fallback response content is a JSON string if the caller expects it
        return {
            "content": json.dumps({
                "error": "AI not available",
                "fallback": True,
                "karma_change": 0,
                "trait_changes": {},
                "message": "AI service unavailable. Using default logic."
            }),
            "model": "fallback",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        }

    def is_available(self) -> bool:
        """Check if AI client is available"""
        return self.client is not None


# Global AI client instance
ai_client = AIClient()


def get_ai_client() -> AIClient:
    """Get the global AI client instance"""
    return ai_client