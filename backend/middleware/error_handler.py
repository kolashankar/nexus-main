"""Error handling middleware."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with structured error messages."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "message": exc.detail,
            "status_code": exc.status_code
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions with clear error messages."""
    # Extract readable error messages
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"][1:])  # Skip 'body'
        message = error["msg"]
        errors.append(f"{field}: {message}")
    
    error_message = "; ".join(errors) if errors else "Validation error"
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": error_message,
            "message": error_message,
            "details": exc.errors(),
            "status_code": 422
        },
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with logging."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error occurred. Please try again later.",
            "message": "Internal server error occurred. Please try again later.",
            "status_code": 500
        },
    )
