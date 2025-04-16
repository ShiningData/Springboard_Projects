#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data validation module for rule-based model inputs.

This module provides validation for input data dictionaries used by the rule-based model.
It ensures all required fields are present and contain valid values according to business rules.

Raw input features and their valid values:
- NameMtch, BusNameMtch: 'Y','N','C','U','MISSING'
- AddressMtch, CityMtch, ZipMtch: 'Y','N','C','U','MISSING'
- StateMtch: 'Y','N','U','MISSING'
- IDTypeMtch, IDStateMtch: 'Y','N','C','U','MISSING'
- IDNoMtch: 'Y','N','U','MISSING'
- SSNMtch, DOBMtch, HmPhoneMtch, WkPhoneMtch: 'Y','N','C','U','MISSING'
- OverallMtchScore: numeric value between 0.0 and 100.0
"""

from typing import Dict, Any, Set, FrozenSet, Union, Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum, auto
from functools import lru_cache
import time
import hashlib
import json
import threading
from cachetools import LRUCache, TTLCache
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Constants for optimization
DEFAULT_RETURN = "N"
MISSING_VALUE = "MISSING"

# Match indicators
Y = "Y"
N = "N"
C = "C"
U = "U"

# Valid values for each feature type
NAME_VALID_VALUES = frozenset({Y, N, C, U, MISSING_VALUE})
ADDRESS_VALID_VALUES = frozenset({Y, N, C, U, MISSING_VALUE})
STATE_VALID_VALUES = frozenset({Y, N, U, MISSING_VALUE})
ID_TYPE_STATE_VALID_VALUES = frozenset({Y, N, C, U, MISSING_VALUE})
ID_NO_VALID_VALUES = frozenset({Y, N, U, MISSING_VALUE})
SSN_DOB_PHONE_VALID_VALUES = frozenset({Y, N, C, U, MISSING_VALUE})

# Score range constants
SCORE_MIN = 0.0
SCORE_MAX = 100.0

# Required fields for validation
REQUIRED_FIELDS = frozenset({
    # Mapped features
    "NameMtch", "BusNameMtch",
    "AddressMtch", "CityMtch", "StateMtch", "ZipMtch",
    "IDTypeMtch", "IDNoMtch", "IDStateMtch",
    # Unmapped features
    "SSNMtch", "DOBMtch", "HmPhoneMtch", "WkPhoneMtch",
    "OverallMtchScore"
})

# Cache configuration
VALIDATION_CACHE_MAX_SIZE = 10000  # Maximum number of entries in the validation cache
VALIDATION_CACHE_TTL = 3600  # Time-to-live for cache entries in seconds (1 hour)
CACHE_CLEAR_INTERVAL = 86400  # Interval for periodic cache clearing in seconds (24 hours)

# Validation result class for better type safety and clarity
@dataclass(frozen=True)
class ValidationResult:
    """Result of data validation with error details if validation failed."""
    valid: bool
    error: Union[str, None] = None
    error_type: Optional['ValidationErrorType'] = None
    field_name: Optional[str] = None

# Error types for more specific error handling
class ValidationErrorType(Enum):
    """Types of validation errors that can occur."""
    MISSING_KEYS = auto()
    UNEXPECTED_KEYS = auto()
    INVALID_SCORE = auto()
    INVALID_SCORE_TYPE = auto()
    INVALID_CATEGORICAL_VALUE = auto()
    INVALID_VALUE = auto()
    MISSING_REQUIRED = auto()
    UNEXPECTED_FIELD = auto()
    INVALID_TYPE = auto()

# Field validation mapping for vectorized validation
# Using a dictionary for O(1) lookups
FIELD_VALIDATION_MAP = {
    # Name fields
    "NameMtch": (NAME_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    "BusNameMtch": (NAME_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    
    # Address fields
    "AddressMtch": (ADDRESS_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    "CityMtch": (ADDRESS_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    "ZipMtch": (ADDRESS_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    "StateMtch": (STATE_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    
    # ID fields
    "IDTypeMtch": (ID_TYPE_STATE_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    "IDStateMtch": (ID_TYPE_STATE_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    "IDNoMtch": (ID_NO_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    
    # Unmapped fields
    "SSNMtch": (SSN_DOB_PHONE_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    "DOBMtch": (SSN_DOB_PHONE_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    "HmPhoneMtch": (SSN_DOB_PHONE_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
    "WkPhoneMtch": (SSN_DOB_PHONE_VALID_VALUES, ValidationErrorType.INVALID_VALUE),
}

# Pre-compute common validation results for performance
@lru_cache(maxsize=1024)
def _compute_data_hash(data_str: str) -> str:
    """Compute a hash of the data for caching validation results."""
    return hashlib.md5(data_str.encode()).hexdigest()

@lru_cache(maxsize=2048)
def normalize_input(value: Any) -> str:
    """
    Normalize input value for consistent comparison.
    
    Args:
        value: The input value to normalize.
        
    Returns:
        str: The normalized value, or MISSING_VALUE if the input is None or empty.
    """
    if value is None:
        return MISSING_VALUE
    
    if not isinstance(value, str):
        return MISSING_VALUE
        
    value = value.strip()
    if not value:  # Check if empty after stripping
        return MISSING_VALUE
        
    return value.upper()

# Thread-safe cache for validation results with size limit and TTL
_validation_cache = TTLCache(maxsize=VALIDATION_CACHE_MAX_SIZE, ttl=VALIDATION_CACHE_TTL)
_cache_lock = threading.Lock()

# Timer for periodic cache clearing
_cache_clear_timer = None

def _schedule_cache_clear():
    """Schedule periodic cache clearing."""
    global _cache_clear_timer
    
    def clear_cache_periodically():
        """Clear cache periodically and reschedule."""
        clear_validation_cache()
        _schedule_cache_clear()
    
    # Cancel existing timer if any
    if _cache_clear_timer:
        _cache_clear_timer.cancel()
    
    # Schedule next cache clear
    _cache_clear_timer = threading.Timer(CACHE_CLEAR_INTERVAL, clear_cache_periodically)
    _cache_clear_timer.daemon = True  # Allow the timer to be garbage collected when the program exits
    _cache_clear_timer.start()

def validate_matches(data: Dict[str, Any]) -> ValidationResult:
    """
    Validate that all the required keys exist in the input data and that
    the values for each key are in the correct form.
    
    This function uses a vectorized approach for improved performance:
    1. Using a field validation map to avoid repeated conditionals
    2. Normalizing all values at once
    3. Checking for missing fields in a single pass
    4. Validating all fields in a single pass
    5. Caching validation results for frequently encountered data
    
    Args:
        data: A dictionary containing feature match information.
            
    Returns:
        ValidationResult: A dataclass with validation result:
            - valid (bool): True if all validations pass, False otherwise
            - error (str): Error message if validation fails, None otherwise
            - error_type (ValidationErrorType): Type of error if validation fails, None otherwise
            - field_name (str): Name of the field that caused the error, None otherwise
    """
    # Fast path: Check if data is None or not a dict
    if not isinstance(data, dict):
        return ValidationResult(
            valid=False,
            error="Input must be a dictionary",
            error_type=ValidationErrorType.INVALID_TYPE,
            field_name=None
        )
    
    # Fast path: Check if data is empty
    if not data:
        return ValidationResult(
            valid=False,
            error="Input dictionary is empty",
            error_type=ValidationErrorType.MISSING_KEYS,
            field_name=None
        )
    
    # Try to get cached result
    try:
        data_str = json.dumps(data, sort_keys=True)
        data_hash = _compute_data_hash(data_str)
        
        # Thread-safe cache access
        with _cache_lock:
            if data_hash in _validation_cache:
                return _validation_cache[data_hash]
    except (TypeError, ValueError):
        # If serialization fails, continue with normal validation
        pass
    
    # Check for unexpected fields - this is a common error case, so check early
    unexpected_fields = set(data.keys()) - REQUIRED_FIELDS
    if unexpected_fields:
        result = ValidationResult(
            valid=False, 
            error=f"Unexpected fields: {', '.join(sorted(unexpected_fields))}",
            error_type=ValidationErrorType.UNEXPECTED_FIELD,
            field_name=list(unexpected_fields)[0]
        )
        # Thread-safe cache update
        with _cache_lock:
            _validation_cache[data_hash] = result
        return result
    
    # Check for missing required fields - another common error case
    missing_fields = REQUIRED_FIELDS - set(data.keys())
    if missing_fields:
        result = ValidationResult(
            valid=False,
            error=f"Missing required fields: {', '.join(sorted(missing_fields))}",
            error_type=ValidationErrorType.MISSING_REQUIRED,
            field_name=list(missing_fields)[0]
        )
        # Thread-safe cache update
        with _cache_lock:
            _validation_cache[data_hash] = result
        return result
    
    # Check for None values and empty strings first
    for field, value in data.items():
        if field != "OverallMtchScore":
            if value is None:
                result = ValidationResult(
                    valid=False,
                    error=f"None value not allowed for field {field}",
                    error_type=ValidationErrorType.INVALID_VALUE,
                    field_name=field
                )
                # Thread-safe cache update
                with _cache_lock:
                    _validation_cache[data_hash] = result
                return result
            elif isinstance(value, str) and not value.strip():
                result = ValidationResult(
                    valid=False,
                    error=f"Empty string not allowed for field {field}",
                    error_type=ValidationErrorType.INVALID_VALUE,
                    field_name=field
                )
                # Thread-safe cache update
                with _cache_lock:
                    _validation_cache[data_hash] = result
                return result
    
    # Normalize all values at once for better performance
    normalized_data = {k: normalize_input(v) for k, v in data.items()}
    
    # Validate all fields except OverallMtchScore
    for field, value in normalized_data.items():
        if field == "OverallMtchScore":
            continue
            
        valid_values, error_type = FIELD_VALIDATION_MAP[field]
        if value not in valid_values:
            result = ValidationResult(
                valid=False,
                error=f"Invalid value for {field}: {value}",
                error_type=error_type,
                field_name=field
            )
            # Thread-safe cache update
            with _cache_lock:
                _validation_cache[data_hash] = result
            return result
    
    # Validate OverallMtchScore separately
    try:
        score = float(data["OverallMtchScore"])
        if not (SCORE_MIN <= score <= SCORE_MAX):
            result = ValidationResult(
                valid=False, 
                error=f"OverallMtchScore must be between {SCORE_MIN} and {SCORE_MAX}, got: {score}",
                error_type=ValidationErrorType.INVALID_SCORE,
                field_name="OverallMtchScore"
            )
            # Thread-safe cache update
            with _cache_lock:
                _validation_cache[data_hash] = result
            return result
    except (ValueError, TypeError):
        result = ValidationResult(
            valid=False,
            error=f"OverallMtchScore must be a number, got: {data['OverallMtchScore']}",
            error_type=ValidationErrorType.INVALID_SCORE_TYPE,
            field_name="OverallMtchScore"
        )
        # Thread-safe cache update
        with _cache_lock:
            _validation_cache[data_hash] = result
        return result
    
    # All validations passed
    result = ValidationResult(valid=True)
    # Thread-safe cache update
    with _cache_lock:
        _validation_cache[data_hash] = result
    return result

def validate_matches_with_error_type(data: Dict[str, Any]) -> Tuple[bool, Union[str, None], Union[ValidationErrorType, None], Union[str, None]]:
    """
    Enhanced validation that also returns the specific error type.
    
    Args:
        data: A dictionary containing feature match information.
            
    Returns:
        Tuple containing:
            - bool: True if valid, False otherwise
            - str: Error message if invalid, None otherwise
            - ValidationErrorType: Type of error if invalid, None otherwise
            - str: Field name that caused the error, None otherwise
    """
    result = validate_matches(data)
    return result.valid, result.error, result.error_type, result.field_name

def clear_validation_cache() -> None:
    """Clear the validation cache to free memory."""
    global _validation_cache
    
    # Thread-safe cache clearing
    with _cache_lock:
        _validation_cache.clear()
        normalize_input.cache_clear()
        _compute_data_hash.cache_clear()
    
    logger.info("Validation cache cleared")

def get_cache_stats() -> Dict[str, Any]:
    """
    Get statistics about the validation cache.
    
    Returns:
        Dict containing cache statistics:
            - validation_cache_size: Number of entries in the validation cache
            - normalize_input_hits: Number of hits in the normalize_input cache
            - normalize_input_misses: Number of misses in the normalize_input cache
            - data_hash_hits: Number of hits in the data hash cache
            - data_hash_misses: Number of misses in the data hash cache
    """
    with _cache_lock:
        return {
            "validation_cache_size": len(_validation_cache),
            "normalize_input_hits": normalize_input.cache_info().hits,
            "normalize_input_misses": normalize_input.cache_info().misses,
            "data_hash_hits": _compute_data_hash.cache_info().hits,
            "data_hash_misses": _compute_data_hash.cache_info().misses
        }

# Initialize periodic cache clearing
_schedule_cache_clear()
