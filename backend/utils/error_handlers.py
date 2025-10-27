"""
Common error handling utilities for API endpoints.
"""
from typing import Callable, Any
from functools import wraps
from fastapi import HTTPException, status


def handle_service_errors(func: Callable) -> Callable:
    """
    Decorator to handle common service errors in API endpoints.
    Converts ValueError to 400 Bad Request and other exceptions to 500 Internal Server Error.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    return wrapper


def handle_action_errors(func: Callable) -> Callable:
    """
    Decorator specifically for action endpoints (hack, help, donate, trade, etc).
    """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Action failed: {str(e)}")
    return wrapper
