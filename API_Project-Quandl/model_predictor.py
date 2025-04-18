#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Monitoring Package

This package provides tools for monitoring API performance and health.
It integrates with FastAPI middleware for automatic request tracking.
"""
import logging
import time
from typing import Dict, Any, Callable, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from collections import defaultdict
import json
from pathlib import Path
from datetime import datetime

# Configure logging
logger = logging.getLogger("acc_auth_api")

# Constants
MAX_HISTORY_SIZE = 1000
PERFORMANCE_LOG_FILE = "performance_metrics.json"
PERFORMANCE_LOG_DIR = Path("logs")

# Ensure log directory exists
PERFORMANCE_LOG_DIR.mkdir(exist_ok=True)

# Store metrics in memory
_request_times = defaultdict(list)
_error_counts = defaultdict(int)
_error_types = defaultdict(lambda: defaultdict(int))

class MonitoringMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for monitoring API performance.
    
    This middleware automatically tracks request latency and errors
    for all API endpoints.
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        logger.info("Initializing monitoring middleware")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and record performance metrics.
        
        Args:
            request: The incoming request
            call_next: The next middleware or route handler
            
        Returns:
            The response from the next handler
        """
        # Record start time
        start_time = time.time()
        
        # Process the request
        try:
            response = await call_next(request)
            
            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000
            
            # Record metrics
            endpoint = request.url.path
            record_api_latency(endpoint, latency_ms)
            
            # Log request information
            logger.info(f"Request to {endpoint} completed in {latency_ms:.2f}ms")
            
            return response
        except Exception as e:
            # Record error
            endpoint = request.url.path
            error_type = type(e).__name__
            error_detail = {"message": str(e)}
            
            record_error(endpoint, error_type, error_detail)
            
            # Re-raise the exception
            raise

def record_api_latency(endpoint: str, latency: float) -> None:
    """
    Record API endpoint latency.
    
    Args:
        endpoint: The API endpoint
        latency: Request processing time in milliseconds
    """
    _request_times[endpoint].append(latency)
    
    # Keep only last MAX_HISTORY_SIZE requests per endpoint
    if len(_request_times[endpoint]) > MAX_HISTORY_SIZE:
        _request_times[endpoint] = _request_times[endpoint][-MAX_HISTORY_SIZE:]
    
    # Periodically save to disk (every 100 records)
    if len(_request_times[endpoint]) % 100 == 0:
        _save_historical_data()

def record_error(endpoint: str, error_type: str = "unknown", error_detail: Dict[str, Any] = None) -> None:
    """
    Record an error for an endpoint.
    
    Args:
        endpoint: The API endpoint where the error occurred
        error_type: The type of error (e.g., "validation_error", "prediction_error")
        error_detail: Additional error details
    """
    _error_counts[endpoint] += 1
    _error_types[endpoint][error_type] += 1
    
    # Log detailed error information if available
    if error_detail:
        logger.error(f"Error in {endpoint}: {error_detail}")

def _save_historical_data() -> None:
    """Save current performance data to disk."""
    log_file = PERFORMANCE_LOG_DIR / PERFORMANCE_LOG_FILE
    try:
        data = {
            "request_times": {k: list(v) for k, v in _request_times.items()},
            "error_counts": dict(_error_counts),
            "error_types": {k: dict(v) for k, v in _error_types.items()}
        }
        
        with open(log_file, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(f"Error saving historical performance data: {e}")

def _load_historical_data() -> None:
    """Load historical performance data from disk if available."""
    log_file = PERFORMANCE_LOG_DIR / PERFORMANCE_LOG_FILE
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                data = json.load(f)
                
                # Load request times
                for endpoint, times in data.get("request_times", {}).items():
                    _request_times[endpoint] = times[-MAX_HISTORY_SIZE:]
                
                # Load error counts
                for endpoint, count in data.get("error_counts", {}).items():
                    _error_counts[endpoint] = count
                
                # Load error types
                for endpoint, types in data.get("error_types", {}).items():
                    for error_type, count in types.items():
                        _error_types[endpoint][error_type] = count
                
            logger.info(f"Loaded historical performance data")
        except Exception as e:
            logger.error(f"Error loading historical performance data: {e}")

def get_performance_report() -> Dict[str, Any]:
    """
    Get performance metrics for all endpoints.
    
    Returns:
        Dictionary containing performance metrics
    """
    report = {
        "timestamp": datetime.now().isoformat(),
        "endpoints": {},
        "summary": {
            "total_endpoints": len(_request_times),
            "total_requests": sum(len(times) for times in _request_times.values()),
            "total_errors": sum(_error_counts.values())
        }
    }
    
    for endpoint in _request_times:
        times = _request_times[endpoint]
        if times:
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            error_count = _error_counts[endpoint]
            
            report["endpoints"][endpoint] = {
                "average_latency_ms": round(avg_time, 2),
                "max_latency_ms": round(max_time, 2),
                "min_latency_ms": round(min_time, 2),
                "request_count": len(times),
                "error_count": error_count,
                "error_types": dict(_error_types[endpoint])
            }
    
    return report

# Load historical data on import
_load_historical_data()

__all__ = [
    "MonitoringMiddleware",
    "record_api_latency",
    "get_performance_report",
    "record_error"
]
