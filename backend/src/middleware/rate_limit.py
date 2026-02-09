from fastapi import HTTPException, status
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict
import time

# Simple in-memory rate limiter (for demonstration purposes)
# In production, use Redis or another distributed store
request_counts: Dict[str, list] = defaultdict(list)

def rate_limit(max_requests: int, window_size: int):
    """
    Rate limiting decorator
    Args:
        max_requests: Maximum number of requests allowed
        window_size: Time window in seconds
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get client IP (this is simplified; in practice, consider X-Forwarded-For headers)
            request = kwargs.get('request') or (args[0] if hasattr(args[0], 'client') else None)
            if request and hasattr(request, 'client'):
                client_ip = request.client.host
            else:
                client_ip = "unknown"
            
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=window_size)
            
            # Clean old requests outside the window
            request_counts[client_ip] = [
                req_time for req_time in request_counts[client_ip] 
                if req_time > window_start
            ]
            
            # Check if limit exceeded
            if len(request_counts[client_ip]) >= max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Maximum {max_requests} requests per {window_size} seconds."
                )
            
            # Add current request to the list
            request_counts[client_ip].append(now)
            
            # Call the original function
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

# Alternative implementation using a class-based approach
class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id: str, max_requests: int, window_size: int) -> bool:
        """
        Check if a client is allowed to make a request
        Args:
            client_id: Unique identifier for the client
            max_requests: Maximum number of requests allowed
            window_size: Time window in seconds
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_size)
        
        # Clean old requests outside the window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id] 
            if req_time > window_start
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= max_requests:
            return False
        
        # Add current request to the list
        self.requests[client_id].append(now)
        return True