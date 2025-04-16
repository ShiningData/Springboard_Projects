#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prediction Service Module

Contains the core prediction logic and validation functions.
"""
from fastapi import HTTPException
from pydantic import ValidationError
from typing import Dict, Any, List, Tuple
import time
import logging
import functools
from cachetools import TTLCache, cached

from models import acc_auth_model
from validate_data import validate_matches
from create_pai_mapping import (
    mapping_address_match,
    mapping_id_match,
    mapping_name_match
)
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

# Dependency for request validation
async def validate_request(request: acc_auth_model) -> Dict[str, Any]:
    """
    Dependency for request validation and conversion.
    
    Args:
        request: The Pydantic model from the request
        
    Returns:
        Dict: Validated dictionary data
    """
    try:
        # Use model_dump() for Pydantic v2 or dict() for v1
        return request.model_dump() if hasattr(request, "model_dump") else request.dict()
    except ValidationError as e:
        logger.error(f"Request validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))


# Cached mapping functions
@cached(cache=mapping_cache)
def cached_name_match(name_match: str, bus_name_match: str) -> str:
    """Cached version of name match mapping"""
    return mapping_name_match(name_match, bus_name_match)

@cached(cache=mapping_cache)
def cached_address_match(address_match: str, city_match: str, state_match: str, zip_match: str) -> str:
    """Cached version of address match mapping"""
    return mapping_address_match(address_match, city_match, state_match, zip_match)

@cached(cache=mapping_cache)
def cached_id_match(id_type_match: str, id_no_match: str, id_state_match: str) -> str:
    """Cached version of ID match mapping"""
    return mapping_id_match(id_type_match, id_no_match, id_state_match)


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
        ValueError: If validation fails due to missing or unexpected
                  values in the input.
    """
    # Start timing
    start_time = time.time()
    
    # Validate required fields exist - use set operations for efficiency
    missing_fields = REQUIRED_FIELDS - set(request_data.keys())
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Normalize input data - handle None and empty values in one pass
    normalized_data = {
        key: "MISSING" if value is None or value == "" else value
        for key, value in request_data.items()
    }
    
    # Generate PAI fields efficiently using cached mapping functions
    pai_values = [
        # PAINameMtch
        cached_name_match(
            normalized_data["NameMtch"],
            normalized_data["BusNameMtch"]
        ),
        # SSNMtch
        normalized_data["SSNMtch"],
        # DOBMtch
        normalized_data["DOBMtch"],
        # PAIAddressMtch
        cached_address_match(
            normalized_data["AddressMtch"],
            normalized_data["CityMtch"],
            normalized_data["StateMtch"],
            normalized_data["ZipMtch"]
        ),
        # HmPhoneMtch
        normalized_data["HmPhoneMtch"],
        # WkPhoneMtch
        normalized_data["WkPhoneMtch"],
        # PAIIDMtch
        cached_id_match(
            normalized_data["IDTypeMtch"],
            normalized_data["IDNoMtch"],
            normalized_data["IDStateMtch"]
        ),
        # OverallMtchScore
        normalized_data["OverallMtchScore"]
    ]
    
    # Create BAA dictionary efficiently
    baa_dict = dict(zip(BAA_COLUMNS, pai_values))
    
    # Determine result code
    result_code = determine_result_code(baa_dict)
    
    # Log performance metrics
    elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    logger.info(f"Prediction completed in {elapsed_time:.2f}ms")
    
    return {"customerResultCode": result_code} 
