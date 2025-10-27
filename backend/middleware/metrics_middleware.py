"""Middleware for collecting request metrics."""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import uuid

from backend.monitoring.metrics import metrics_collector
from backend.monitoring.logger import RequestLogger

request_logger = RequestLogger()


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect request metrics."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Record start time
        start_time = time.time()

        # Process request
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            status_code = 500
            raise
        finally:
            # Calculate duration
            duration = time.time() - start_time

            # Record metrics
            metrics_collector.record_request(
                endpoint=request.url.path,
                method=request.method,
                status=status_code,
                duration=duration
            )

            # Log request
            request_logger.log_request(
                method=request.method,
                path=request.url.path,
                status=status_code,
                duration=duration,
                request_id=request_id
            )

        # Add metrics headers
        response.headers['X-Request-ID'] = request_id
        response.headers['X-Response-Time'] = f"{duration:.3f}"

        return response
