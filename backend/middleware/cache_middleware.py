"""Cache Middleware for AI Responses"""

import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

logger = logging.getLogger(__name__)


class AICacheMiddleware(BaseHTTPMiddleware):
    """Middleware to handle AI response caching"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request through cache layer"""

        # Check if this is an AI endpoint
        if "/api/v1/ai/" in str(request.url):
            logger.debug(f"AI request: {request.method} {request.url.path}")

        # Process request
        response = await call_next(request)

        # Add cache headers for AI responses
        if "/api/v1/ai/" in str(request.url):
            response.headers["X-AI-Service"] = "karma-nexus"

        return response
