"""
Common response helper utilities for API endpoints.
"""
from typing import Dict, Any


def success_response(message: str, **kwargs) -> Dict[str, Any]:
    """
    Create a standard success response.
    
    Args:
        message: Success message
        **kwargs: Additional fields to include in response
        
    Returns:
        Dictionary with success=True, message, and any additional fields
    """
    return {
        "success": True,
        "message": message,
        **kwargs
    }


def error_response(message: str, **kwargs) -> Dict[str, Any]:
    """
    Create a standard error response.
    
    Args:
        message: Error message
        **kwargs: Additional fields to include in response
        
    Returns:
        Dictionary with success=False, message, and any additional fields
    """
    return {
        "success": False,
        "error": message,
        **kwargs
    }
