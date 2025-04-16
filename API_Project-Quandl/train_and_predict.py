#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load Testing Script for Rule Engine API

This script performs load testing on the API endpoints to measure latency performance.
It tests both the prediction endpoint and the health check endpoint under various load conditions.
"""
import asyncio
import time
import statistics
import json
from typing import Dict, List, Any, Tuple
import httpx
import argparse
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import numpy as np

# Test data scenarios for each CRC code
TEST_SCENARIOS = {
    "CRC1000": {  # Pass - Perfect match
        "NameMtch": "Y",
        "BusNameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "AddressMtch": "Y",
        "CityMtch": "Y",
        "StateMtch": "Y",
        "ZipMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "IDTypeMtch": "Y",
        "IDNoMtch": "Y",
        "IDStateMtch": "Y",
        "OverallMtchScore": 95
    },
    "CRC2100": {  # Caution - Address mismatch
        "NameMtch": "Y",
        "BusNameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "AddressMtch": "N",
        "CityMtch": "Y",
        "StateMtch": "Y",
        "ZipMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "IDTypeMtch": "Y",
        "IDNoMtch": "Y",
        "IDStateMtch": "Y",
        "OverallMtchScore": 85
    },
    "CRC2200": {  # Caution - Phone mismatch
        "NameMtch": "Y",
        "BusNameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "AddressMtch": "Y",
        "CityMtch": "Y",
        "StateMtch": "Y",
        "ZipMtch": "Y",
        "HmPhoneMtch": "N",
        "WkPhoneMtch": "Y",
        "IDTypeMtch": "Y",
        "IDNoMtch": "Y",
        "IDStateMtch": "Y",
        "OverallMtchScore": 85
    },
    "CRC2300": {  # Caution - ID mismatch
        "NameMtch": "Y",
        "BusNameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "AddressMtch": "Y",
        "CityMtch": "Y",
        "StateMtch": "Y",
        "ZipMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "IDTypeMtch": "Y",
        "IDNoMtch": "N",
        "IDStateMtch": "Y",
        "OverallMtchScore": 85
    },
    "CRC3100": {  # Warning - Name mismatch
        "NameMtch": "N",
        "BusNameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "AddressMtch": "Y",
        "CityMtch": "Y",
        "StateMtch": "Y",
        "ZipMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "IDTypeMtch": "Y",
        "IDNoMtch": "Y",
        "IDStateMtch": "Y",
        "OverallMtchScore": 75
    },
    "CRC3200": {  # Warning - Tax ID mismatch
        "NameMtch": "Y",
        "BusNameMtch": "Y",
        "SSNMtch": "N",
        "DOBMtch": "Y",
        "AddressMtch": "Y",
        "CityMtch": "Y",
        "StateMtch": "Y",
        "ZipMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "IDTypeMtch": "Y",
        "IDNoMtch": "Y",
        "IDStateMtch": "Y",
        "OverallMtchScore": 75
    },
    "CRC3300": {  # Warning - DOB mismatch
        "NameMtch": "Y",
        "BusNameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "N",
        "AddressMtch": "Y",
        "CityMtch": "Y",
        "StateMtch": "Y",
        "ZipMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "IDTypeMtch": "Y",
        "IDNoMtch": "Y",
        "IDStateMtch": "Y",
        "OverallMtchScore": 75
    },
    "CRC3900": {  # Warning - Multiple mismatches
        "NameMtch": "Y",
        "BusNameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "AddressMtch": "N",
        "CityMtch": "Y",
        "StateMtch": "Y",
        "ZipMtch": "Y",
        "HmPhoneMtch": "N",
        "WkPhoneMtch": "Y",
        "IDTypeMtch": "Y",
        "IDNoMtch": "Y",
        "IDStateMtch": "Y",
        "OverallMtchScore": 65
    },
    "CRC4000": {  # Decline - Score below threshold
        "NameMtch": "Y",
        "BusNameMtch": "Y",
        "SSNMtch": "N",
        "DOBMtch": "N",
        "AddressMtch": "N",
        "CityMtch": "Y",
        "StateMtch": "Y",
        "ZipMtch": "Y",
        "HmPhoneMtch": "N",
        "WkPhoneMtch": "N",
        "IDTypeMtch": "Y",
        "IDNoMtch": "N",
        "IDStateMtch": "Y",
        "OverallMtchScore": 25
    },
    "CRC0000": {  # Inconclusive - Missing data
        "NameMtch": "MISSING",
        "BusNameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "AddressMtch": "Y",
        "CityMtch": "Y",
        "StateMtch": "Y",
        "ZipMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "IDTypeMtch": "Y",
        "IDNoMtch": "Y",
        "IDStateMtch": "Y",
        "OverallMtchScore": 95
    }
}

# API endpoints
PREDICTION_ENDPOINT = "http://localhost:8000/get-result-code"
HEALTH_ENDPOINT = "http://localhost:8000/health"

async def make_request(client: httpx.AsyncClient, endpoint: str, data: Dict[str, Any] = None) -> Tuple[float, int, str]:
    """
    Make a request to the specified endpoint and measure latency.
    
    Args:
        client: The httpx client
        endpoint: The API endpoint to test
        data: The data to send (for POST requests)
        
    Returns:
        Tuple containing the latency in milliseconds, status code, and response body
    """
    start_time = time.time()
    
    try:
        if data:
            response = await client.post(endpoint, json=data)
        else:
            response = await client.get(endpoint)
        
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds
        return latency, response.status_code, response.text
    except Exception as e:
        print(f"Error making request: {e}")
        return -1, -1, str(e)

async def run_load_test(endpoint: str, data: Dict[str, Any] = None, 
                        num_requests: int = 100, concurrency: int = 10) -> List[Tuple[float, int, str]]:
    """
    Run a load test on the specified endpoint.
    
    Args:
        endpoint: The API endpoint to test
        data: The data to send (for POST requests)
        num_requests: The number of requests to make
        concurrency: The number of concurrent requests
        
    Returns:
        List of tuples containing latencies, status codes, and responses
    """
    results = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = []
        for _ in range(num_requests):
            tasks.append(make_request(client, endpoint, data))
            
            # Process in batches based on concurrency
            if len(tasks) >= concurrency:
                batch_results = await asyncio.gather(*tasks)
                results.extend([r for r in batch_results if r[0] > 0])
                tasks = []
        
        # Process any remaining tasks
        if tasks:
            batch_results = await asyncio.gather(*tasks)
            results.extend([r for r in batch_results if r[0] > 0])
    
    return results

def calculate_statistics(results: List[Tuple[float, int, str]]) -> Dict[str, Any]:
    """
    Calculate statistics for the latencies and responses.
    
    Args:
        results: List of tuples containing latencies, status codes, and responses
        
    Returns:
        Dictionary containing statistics and response distribution
    """
    if not results:
        return {
            "min": 0,
            "max": 0,
            "mean": 0,
            "median": 0,
            "p95": 0,
            "p99": 0,
            "response_codes": {},
            "status_codes": {}
        }
    
    latencies = [r[0] for r in results]
    status_codes = {}
    response_codes = {}
    
    for _, status, response in results:
        status_codes[status] = status_codes.get(status, 0) + 1
        try:
            response_data = json.loads(response)
            if "customerResultcode" in response_data:
                response_codes[response_data["customerResultcode"]] = response_codes.get(response_data["customerResultcode"], 0) + 1
        except:
            pass
    
    return {
        "min": min(latencies),
        "max": max(latencies),
        "mean": statistics.mean(latencies),
        "median": statistics.median(latencies),
        "p95": np.percentile(latencies, 95),
        "p99": np.percentile(latencies, 99),
        "response_codes": response_codes,
        "status_codes": status_codes
    }

def plot_latency_distribution(latencies: List[float], title: str, filename: str):
    """
    Plot the latency distribution.
    
    Args:
        latencies: List of latencies in milliseconds
        title: Title for the plot
        filename: Filename to save the plot
    """
    plt.figure(figsize=(10, 6))
    plt.hist(latencies, bins=50, alpha=0.7, color='blue')
    plt.axvline(statistics.mean(latencies), color='red', linestyle='dashed', linewidth=1, label=f'Mean: {statistics.mean(latencies):.2f}ms')
    plt.axvline(statistics.median(latencies), color='green', linestyle='dashed', linewidth=1, label=f'Median: {statistics.median(latencies):.2f}ms')
    plt.axvline(np.percentile(latencies, 95), color='purple', linestyle='dashed', linewidth=1, label=f'95th percentile: {np.percentile(latencies, 95):.2f}ms')
    plt.title(title)
    plt.xlabel('Latency (ms)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(filename)
    plt.close()

async def main():
    parser = argparse.ArgumentParser(description='Load test the Rule Engine API')
    parser.add_argument('--scenario', type=str, choices=list(TEST_SCENARIOS.keys()) + ['all'],
                        help='Scenario to test (default: all)')
    parser.add_argument('--requests', type=int, default=100, help='Number of requests to make (default: 100)')
    parser.add_argument('--concurrency', type=int, default=10, help='Number of concurrent requests (default: 10)')
    parser.add_argument('--plot', action='store_true', help='Generate latency distribution plots')
    
    args = parser.parse_args()
    
    print(f"Starting load test with {args.requests} requests and concurrency of {args.concurrency}")
    
    results = {}
    
    # Test each scenario
    scenarios_to_test = [args.scenario] if args.scenario and args.scenario != 'all' else TEST_SCENARIOS.keys()
    
    for scenario in scenarios_to_test:
        print(f"\n=== Testing Scenario: {scenario} ===")
        test_data = TEST_SCENARIOS[scenario]
        
        # Run the load test
        test_results = await run_load_test(PREDICTION_ENDPOINT, test_data, args.requests, args.concurrency)
        stats = calculate_statistics(test_results)
        
        # Print statistics
        print(f"Statistics for {scenario}:")
        print(f"  Min: {stats['min']:.2f}ms")
        print(f"  Max: {stats['max']:.2f}ms")
        print(f"  Mean: {stats['mean']:.2f}ms")
        print(f"  Median: {stats['median']:.2f}ms")
        print(f"  95th percentile: {stats['p95']:.2f}ms")
        print(f"  99th percentile: {stats['p99']:.2f}ms")
        print("\nResponse Code Distribution:")
        for code, count in stats['response_codes'].items():
            print(f"  {code}: {count} requests")
        
        # Generate plot if requested
        if args.plot:
            plot_latency_distribution(
                [r[0] for r in test_results],
                f'Latency Distribution - {scenario}',
                f'latency_{scenario}.png'
            )
        
        results[scenario] = {
            "statistics": stats,
            "latencies": [r[0] for r in test_results]
        }
    
    # Save all results to JSON file
    with open('load_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to load_test_results.json")

if __name__ == "__main__":
    asyncio.run(main()) 
