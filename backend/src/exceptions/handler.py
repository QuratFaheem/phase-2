from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base API exception class"""
    def __init__(self, code: str, message: str, status_code: int = 400, details: dict = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(APIError):
    """Raised when request validation fails"""
    def __init__(self, message: str = "Validation error", details: dict = None):
        super().__init__("VALIDATION_ERROR", message, 422, details)

class AuthenticationError(APIError):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__("AUTHENTICATION_ERROR", message, 401)

class AuthorizationError(APIError):
    """Raised when authorization fails"""
    def __init__(self, message: str = "Not authorized"):
        super().__init__("AUTHORIZATION_ERROR", message, 403)

class ResourceNotFoundError(APIError):
    """Raised when a requested resource is not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__("RESOURCE_NOT_FOUND", message, 404)

class BusinessLogicError(APIError):
    """Raised when business logic validation fails"""
    def __init__(self, message: str = "Business logic error"):
        super().__init__("BUSINESS_LOGIC_ERROR", message, 400)

def api_error_handler(exc: APIError) -> JSONResponse:
    """Standardized error response format"""
    logger.error(f"API Error: {exc.code} - {exc.message}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTPException with standardized format"""
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": str(exc.detail),
                "details": {}
            }
        }
    )

def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions with standardized format"""
    logger.error(f"General Exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal server error occurred",
                "details": {}
            }
        }
    )

# Success response helper
def success_response(data=None, message: str = "Request successful") -> dict:
    """Standardized success response format"""
    response = {
        "success": True,
        "message": message
    }
    
    if data is not None:
        response["data"] = data
    
    return response