#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prediction Service Module

Contains the core prediction logic and validation functions.
"""
from fastapi import HTTPException, status
from pydantic import ValidationError
from typing import Dict, Any, Optional
import time
import logging
import functools
from cachetools import TTLCache, cached
import threading

from models import AccAuthModel, MatchStatus
from validate_data import validate_matches, ValidationResult
from create_pai_mapping import create_pai_features
from rule_base_model import determine_result_code

# Configure logging
logger = logging.getLogger("acc_auth_api")

# Pre-defined constants for optimization
REQUIRED_FIELDS = frozenset([
    "NameMtch", "BusNameMtch", "SSNMtch", "DOBMtch", "AddressMtch", 
    "CityMtch", "StateMtch", "ZipMtch", "HmPhoneMtch", "WkPhoneMtch", 
    "IDTypeMtch", "IDNoMtch", "IDStateMtch", "OverallMtchScore"
])

BAA_COLUMNS = [
    "PAINameMtch", "SSNMtch", "DOBMtch", "PAIAddressMtch",
    "HmPhoneMtch", "WkPhoneMtch", "PAIIDMtch", "OverallMtchScore",
]

# Cache for mapping functions with 1-hour TTL
mapping_cache = TTLCache(maxsize=1000, ttl=3600)

# Cache for prediction results with 5-minute TTL
# Using a thread-safe cache for concurrent access
prediction_cache = TTLCache(maxsize=10000, ttl=300)
_cache_lock = threading.Lock()

# Dependency for request validation
async def validate_request(request: AccAuthModel) -> Dict[str, Any]:
    """
    Dependency for request validation and conversion.
    
    Args:
        request: The Pydantic model from the request
        
    Returns:
        Dict: Validated dictionary data
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        # Use model_dump() for Pydantic v2 or dict() for v1
        data_dict = request.model_dump() if hasattr(request, "model_dump") else request.dict()
        
        # Validate the data using the custom validation function
        validation_result = validate_matches(data_dict)
        if not validation_result.valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": validation_result.error,
                    "type": validation_result.error_type.name if validation_result.error_type else "validation_error",
                    "field": validation_result.field_name
                }
            )
            
        return data_dict
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValidationError as e:
        logger.error(f"Request validation error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during validation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error validating request", "type": "validation_error"}
        )

# Core prediction logic
def acc_auth_prediction(request_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Predict the customer result code based on match statuses from
    an input request.
    
    Parameters:
        request_data (dict): A dictionary containing feature match information for
        various customer attributes.
            
    Returns:
        dict: A dictionary containing the customer result code
        ('customerResultCode') after evaluating the matches.
        
    Raises:
        HTTPException: If validation fails due to missing or unexpected
                  values in the input.
    """
    # Start timing
    start_time = time.time()
    
    try:
        # Check cache first with thread safety
        cache_key = _generate_cache_key(request_data)
        with _cache_lock:
            if cache_key in prediction_cache:
                logger.info("Prediction result retrieved from cache")
                return prediction_cache[cache_key]
        
        # Validate the data using the custom validation function
        validation_result = validate_matches(request_data)
        if not validation_result.valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": validation_result.error,
                    "type": validation_result.error_type.name if validation_result.error_type else "validation_error",
                    "field": validation_result.field_name
                }
            )
        
        # Use the create_pai_features function to map the input fields to PAI features
        mapped_data = create_pai_features(request_data)
        
        # Determine result code
        result_code = determine_result_code(mapped_data)
        
        # Cache the result with thread safety
        result = {"customerResultCode": result_code}
        with _cache_lock:
            prediction_cache[cache_key] = result
        
        # Log performance metrics
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Prediction completed in {elapsed_time:.2f}ms")
        
        return result
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error with more context
        logger.error(f"Error determining result code: {str(e)}", exc_info=True)
        # Raise HTTP exception with appropriate status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={"message": "Error determining result code", "type": "prediction_error"}
        )

def _generate_cache_key(data: Dict[str, Any]) -> str:
    """
    Generate a cache key from the input data.
    
    Args:
        data: Input data dictionary
        
    Returns:
        str: Cache key
    """
    # Sort the dictionary to ensure consistent keys
    sorted_data = {k: data[k] for k in sorted(data.keys())}
    # Convert to string and hash
    data_str = str(sorted_data)
    return hash(data_str)

# Clear caches
def clear_caches() -> None:
    """
    Clear all caches used by the prediction service.
    """
    with _cache_lock:
        mapping_cache.clear()
        prediction_cache.clear()
    logger.info("All prediction service caches cleared") 
