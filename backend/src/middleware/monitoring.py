from fastapi import Request, Response
from typing import Callable, Awaitable
import time
import logging
from collections import defaultdict, deque
from datetime import datetime, timedelta
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricsCollector:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.response_times = deque(maxlen=1000)  # Keep last 1000 response times
        self.status_codes = defaultdict(int)
        self.lock = threading.Lock()
    
    def record_request(self, response_time: float, status_code: int):
        with self.lock:
            self.request_count += 1
            self.response_times.append(response_time)
            self.status_codes[status_code] += 1
            if 400 <= status_code < 600:
                self.error_count += 1
    
    def get_metrics(self):
        with self.lock:
            if not self.response_times:
                avg_response_time = 0
                p95_response_time = 0
            else:
                sorted_times = sorted(self.response_times)
                avg_response_time = sum(sorted_times) / len(sorted_times)
                
                # Calculate 95th percentile
                p95_index = int(0.95 * len(sorted_times))
                p95_response_time = sorted_times[min(p95_index, len(sorted_times) - 1)]
            
            error_rate = self.error_count / self.request_count if self.request_count > 0 else 0
            
            return {
                "total_requests": self.request_count,
                "total_errors": self.error_count,
                "error_rate": round(error_rate, 4),
                "average_response_time": round(avg_response_time, 4),
                "p95_response_time": round(p95_response_time, 4),
                "status_codes": dict(self.status_codes),
                "active_requests": 0  # Would need additional tracking
            }

# Global metrics collector instance
metrics_collector = MetricsCollector()

async def monitoring_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """
    Middleware to monitor API performance and collect metrics
    """
    start_time = time.time()
    
    try:
        response = await call_next(request)
    finally:
        process_time = time.time() - start_time
        metrics_collector.record_request(process_time, response.status_code)
        
        # Log request info
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Time: {process_time:.4f}s"
        )
    
    return response

# Endpoint to get metrics
from fastapi import APIRouter

router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    return metrics_collector.get_metrics()