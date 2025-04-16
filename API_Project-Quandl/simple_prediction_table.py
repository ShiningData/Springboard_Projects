#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Middleware Module

Contains custom middleware for the FastAPI application.
"""
import time
import logging
from typing import Callable, Dict, Tuple
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.responses import JSONResponse
from datetime import datetime, timedelta

from monitoring import record_api_latency

# Configure logging
logger = logging.getLogger("acc_auth_api")


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add a process time header to the response.
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate process time
        process_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Add header to response
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        
        # Record latency for performance monitoring
        record_api_latency(request.url.path, process_time)
        
        # Log slow requests
        if process_time > 200:  # Log requests taking more than 200ms
            logger.warning(f"Slow request to {request.url.path}: {process_time:.2f}ms")
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to implement rate limiting.
    
    This middleware tracks the number of requests from each client IP
    and returns a 429 Too Many Requests response if the limit is exceeded.
    """
    def __init__(self, app: ASGIApp, requests: int = 100, period: int = 60):
        super().__init__(app)
        self.requests = requests  # Maximum number of requests
        self.period = period      # Time period in seconds
        self.clients: Dict[str, Tuple[int, datetime]] = {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Get current time
        now = datetime.now()
        
        # Check if client exists in tracking
        if client_ip in self.clients:
            count, last_reset = self.clients[client_ip]
            
            # Check if period has elapsed, reset if needed
            if (now - last_reset).total_seconds() > self.period:
                count = 0
                last_reset = now
            
            # Increment count
            count += 1
            
            # Check if limit exceeded
            if count > self.requests:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Too many requests",
                        "retry_after": self.period - (now - last_reset).total_seconds()
                    }
                )
            
            # Update client tracking
            self.clients[client_ip] = (count, last_reset)
        else:
            # First request from this client
            self.clients[client_ip] = (1, now)
        
        # Process the request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests)
        response.headers["X-RateLimit-Remaining"] = str(
            self.requests - self.clients[client_ip][0]
        )
        response.headers["X-RateLimit-Reset"] = str(
            int((self.clients[client_ip][1] + timedelta(seconds=self.period)).timestamp())
        )
        
        return response


# Function to add process time header (for backward compatibility)
async def add_process_time_header(request: Request, call_next: Callable) -> Response:
    """
    Add a process time header to the response.
    
    Args:
        request: The request object
        call_next: The next middleware or route handler
        
    Returns:
        The response with the process time header
    """
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate process time
    process_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Add header to response
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    
    # Record latency for performance monitoring
    record_api_latency(request.url.path, process_time)
    
    # Log slow requests
    if process_time > 200:  # Log requests taking more than 200ms
        logger.warning(f"Slow request to {request.url.path}: {process_time:.2f}ms")
    
    return response 
