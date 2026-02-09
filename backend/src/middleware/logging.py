from fastapi import Request, Response
from fastapi.responses import StreamingResponse
import time
import logging
from typing import Callable, Awaitable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def logging_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """
    Middleware to log incoming requests and outgoing responses
    """
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    # Process the request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Process time: {process_time:.4f}s")
    
    # Add process time to response headers
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Alternative implementation as a class
class LoggingMiddleware:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Create handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start_time = time.time()
        
        # Log request
        self.logger.info(f"Request: {request.method} {request.url}")
        self.logger.info(f"Client Host: {request.client.host}")
        self.logger.info(f"Headers: {dict(request.headers)}")
        
        try:
            response = await call_next(request)
        except Exception as e:
            # Log exceptions
            self.logger.error(f"Request failed with exception: {str(e)}")
            raise
        finally:
            process_time = time.time() - start_time
            
            # Log response
            self.logger.info(f"Response status: {response.status_code}")
            self.logger.info(f"Process time: {process_time:.4f}s")
            
            # Add process time to response headers
            response.headers["X-Process-Time"] = str(process_time)
        
        return response