#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Monitoring Package

This package provides tools for monitoring API performance and health.
"""

from .performance import record_api_latency, get_performance_report
from typing import Dict, Any
import logging
import time
from collections import defaultdict

# Configure logging
logger = logging.getLogger("acc_auth_api")

# Store metrics in memory
_request_times = defaultdict(list)
_error_counts = defaultdict(int)

async def initialize_monitoring():
    """Initialize monitoring system."""
    logger.info("Initializing monitoring system")
    # Clear existing metrics
    _request_times.clear()
    _error_counts.clear()

async def shutdown_monitoring():
    """Shutdown monitoring system."""
    logger.info("Shutting down monitoring system")
    # Perform any cleanup if needed
    _request_times.clear()
    _error_counts.clear()

def record_api_latency(endpoint: str, latency: float) -> None:
    """
    Record API endpoint latency.
    
    Args:
        endpoint: The API endpoint
        latency: Request processing time in milliseconds
    """
    _request_times[endpoint].append(latency)
    
    # Keep only last 1000 requests per endpoint
    if len(_request_times[endpoint]) > 1000:
        _request_times[endpoint] = _request_times[endpoint][-1000:]

def record_error(endpoint: str) -> None:
    """
    Record an error for an endpoint.
    
    Args:
        endpoint: The API endpoint where the error occurred
    """
    _error_counts[endpoint] += 1

def get_performance_report() -> Dict[str, Any]:
    """
    Get performance metrics for all endpoints.
    
    Returns:
        Dictionary containing performance metrics
    """
    report = {}
    
    for endpoint in _request_times:
        times = _request_times[endpoint]
        if times:
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            error_count = _error_counts[endpoint]
            
            report[endpoint] = {
                "average_latency_ms": round(avg_time, 2),
                "max_latency_ms": round(max_time, 2),
                "min_latency_ms": round(min_time, 2),
                "request_count": len(times),
                "error_count": error_count
            }
    
    return report

__all__ = [
    "record_api_latency",
    "get_performance_report",
    "initialize_monitoring",
    "shutdown_monitoring",
    "record_error"
] 

=================================================================================


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Performance Monitoring Module

This module provides tools for monitoring and analyzing API performance metrics.
"""
import time
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import statistics
from collections import deque
from threading import Lock

# Configure logging
logger = logging.getLogger("acc_auth_api")

# Constants
MAX_HISTORY_SIZE = 1000
PERFORMANCE_LOG_FILE = "performance_metrics.json"
PERFORMANCE_LOG_DIR = Path("logs")

# Ensure log directory exists
PERFORMANCE_LOG_DIR.mkdir(exist_ok=True)


class PerformanceMonitor:
    """
    A class to monitor and record API performance metrics.
    
    This class provides methods to record latency metrics for API endpoints
    and generate performance reports.
    """
    def __init__(self, max_history_size: int = MAX_HISTORY_SIZE):
        """
        Initialize the performance monitor.
        
        Args:
            max_history_size: Maximum number of metrics to keep in memory
        """
        self.max_history_size = max_history_size
        self.metrics: Dict[str, deque] = {}
        self.lock = Lock()
        self._load_historical_data()
    
    def _load_historical_data(self) -> None:
        """Load historical performance data from disk if available."""
        log_file = PERFORMANCE_LOG_DIR / PERFORMANCE_LOG_FILE
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    data = json.load(f)
                    for endpoint, metrics in data.items():
                        self.metrics[endpoint] = deque(metrics[-self.max_history_size:], 
                                                      maxlen=self.max_history_size)
                logger.info(f"Loaded historical performance data for {len(self.metrics)} endpoints")
            except Exception as e:
                logger.error(f"Error loading historical performance data: {e}")
    
    def _save_historical_data(self) -> None:
        """Save current performance data to disk."""
        log_file = PERFORMANCE_LOG_DIR / PERFORMANCE_LOG_FILE
        try:
            with open(log_file, 'w') as f:
                json.dump({k: list(v) for k, v in self.metrics.items()}, f)
        except Exception as e:
            logger.error(f"Error saving historical performance data: {e}")
    
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        """
        Record latency for an API endpoint.
        
        Args:
            endpoint: The API endpoint path
            latency_ms: Latency in milliseconds
        """
        with self.lock:
            if endpoint not in self.metrics:
                self.metrics[endpoint] = deque(maxlen=self.max_history_size)
            
            self.metrics[endpoint].append({
                "timestamp": datetime.now().isoformat(),
                "latency_ms": latency_ms
            })
            
            # Periodically save to disk (every 100 records)
            if len(self.metrics[endpoint]) % 100 == 0:
                self._save_historical_data()
    
    def get_endpoint_statistics(self, endpoint: str) -> Dict[str, float]:
        """
        Get statistics for a specific endpoint.
        
        Args:
            endpoint: The API endpoint path
            
        Returns:
            Dictionary with statistics (min, max, mean, median, p95, p99)
        """
        with self.lock:
            if endpoint not in self.metrics or not self.metrics[endpoint]:
                return {
                    "min": 0,
                    "max": 0,
                    "mean": 0,
                    "median": 0,
                    "p95": 0,
                    "p99": 0
                }
            
            latencies = [m["latency_ms"] for m in self.metrics[endpoint]]
            
            return {
                "min": min(latencies),
                "max": max(latencies),
                "mean": statistics.mean(latencies),
                "median": statistics.median(latencies),
                "p95": self._percentile(latencies, 95),
                "p99": self._percentile(latencies, 99)
            }
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """
        Calculate the percentile value from a list of numbers.
        
        Args:
            data: List of numbers
            percentile: Percentile to calculate (0-100)
            
        Returns:
            The percentile value
        """
        if not data:
            return 0
        
        sorted_data = sorted(data)
        index = (len(sorted_data) - 1) * percentile / 100
        floor = int(index)
        ceil = min(floor + 1, len(sorted_data) - 1)
        
        if floor == ceil:
            return sorted_data[floor]
        
        d0 = sorted_data[floor] * (ceil - index)
        d1 = sorted_data[ceil] * (index - floor)
        return d0 + d1
    
    def get_all_statistics(self) -> Dict[str, Dict[str, float]]:
        """
        Get statistics for all endpoints.
        
        Returns:
            Dictionary with endpoint statistics
        """
        return {
            endpoint: self.get_endpoint_statistics(endpoint)
            for endpoint in self.metrics
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive performance report.
        
        Returns:
            Dictionary with performance report data
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "endpoints": self.get_all_statistics(),
            "summary": {
                "total_endpoints": len(self.metrics),
                "total_requests": sum(len(metrics) for metrics in self.metrics.values())
            }
        }
        
        # Add overall statistics if there are metrics
        if self.metrics:
            all_latencies = [
                m["latency_ms"] 
                for metrics in self.metrics.values() 
                for m in metrics
            ]
            
            report["overall"] = {
                "min": min(all_latencies),
                "max": max(all_latencies),
                "mean": statistics.mean(all_latencies),
                "median": statistics.median(all_latencies),
                "p95": self._percentile(all_latencies, 95),
                "p99": self._percentile(all_latencies, 99)
            }
        
        return report


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def record_api_latency(endpoint: str, latency_ms: float) -> None:
    """
    Record API endpoint latency.
    
    Args:
        endpoint: The API endpoint path
        latency_ms: Latency in milliseconds
    """
    performance_monitor.record_latency(endpoint, latency_ms)


def get_performance_report() -> Dict[str, Any]:
    """
    Get a performance report for all endpoints.
    
    Returns:
        Dictionary with performance report data
    """
    return performance_monitor.generate_report() 
