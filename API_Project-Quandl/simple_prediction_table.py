#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for validate_data.py
"""
import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validate_data import (
    ValidationResult,
    ValidationErrorType,
    normalize_input,
    validate_matches,
    Y,
    N,
    U,
    C,
    MISSING_VALUE,
    REQUIRED_FIELDS
)

# Test ValidationResult class
def test_validation_result():
    """Test the ValidationResult class with various inputs"""
    # Test with no errors
    result = ValidationResult(valid=True)
    assert result.valid is True
    assert result.error is None
    assert result.error_type is None
    assert result.field_name is None
    
    # Test with errors
    result = ValidationResult(
        valid=False,
        error="Invalid value",
        error_type=ValidationErrorType.INVALID_VALUE,
        field_name="NameMtch"
    )
    assert result.valid is False
    assert result.error == "Invalid value"
    assert result.error_type == ValidationErrorType.INVALID_VALUE
    assert result.field_name == "NameMtch"

# Test normalize_input function
def test_normalize_input():
    """Test the normalize_input function with various inputs"""
    # Test with None
    assert normalize_input(None) == MISSING_VALUE
    
    # Test with empty string
    assert normalize_input("") == MISSING_VALUE
    
    # Test with valid string
    assert normalize_input("Y") == Y
    assert normalize_input("N") == N
    assert normalize_input("U") == U
    assert normalize_input("C") == C
    
    # Test with whitespace
    assert normalize_input(" Y ") == Y
    assert normalize_input(" N ") == N
    assert normalize_input(" U ") == U
    assert normalize_input(" C ") == C
    
    # Test with case
    assert normalize_input("y") == Y
    assert normalize_input("n") == N
    assert normalize_input("u") == U
    assert normalize_input("c") == C

# Test validate_matches function
def test_validate_matches():
    """Test the validate_matches function with various inputs"""
    # Test with valid data
    data = {
        "NameMtch": Y,
        "BusNameMtch": Y,
        "AddressMtch": Y,
        "CityMtch": Y,
        "StateMtch": Y,
        "ZipMtch": Y,
        "IDTypeMtch": Y,
        "IDNoMtch": Y,
        "IDStateMtch": Y,
        "SSNMtch": Y,
        "DOBMtch": Y,
        "HmPhoneMtch": Y,
        "WkPhoneMtch": Y,
        "OverallMtchScore": 95.0
    }
    
    result = validate_matches(data)
    assert result.valid is True
    assert result.error is None
    
    # Test with missing required fields
    data = {
        "NameMtch": Y,
        "BusNameMtch": Y,
        "AddressMtch": Y,
        "CityMtch": Y,
        "StateMtch": Y,
        "ZipMtch": Y,
        "IDTypeMtch": Y,
        "IDNoMtch": Y,
        "IDStateMtch": Y,
        "SSNMtch": Y,
        "DOBMtch": Y,
        "HmPhoneMtch": Y,
        "WkPhoneMtch": Y
    }
    
    result = validate_matches(data)
    assert result.valid is False
    assert result.error_type == ValidationErrorType.MISSING_REQUIRED
    assert "OverallMtchScore" in result.error
    
    # Test with invalid values
    data = {
        "NameMtch": "X",
        "BusNameMtch": Y,
        "AddressMtch": Y,
        "CityMtch": Y,
        "StateMtch": Y,
        "ZipMtch": Y,
        "IDTypeMtch": Y,
        "IDNoMtch": Y,
        "IDStateMtch": Y,
        "SSNMtch": Y,
        "DOBMtch": Y,
        "HmPhoneMtch": Y,
        "WkPhoneMtch": Y,
        "OverallMtchScore": 95.0
    }
    
    result = validate_matches(data)
    assert result.valid is False
    assert result.error_type == ValidationErrorType.INVALID_VALUE
    assert result.field_name == "NameMtch"
    
    # Test with None values
    data = {
        "NameMtch": None,
        "BusNameMtch": Y,
        "AddressMtch": Y,
        "CityMtch": Y,
        "StateMtch": Y,
        "ZipMtch": Y,
        "IDTypeMtch": Y,
        "IDNoMtch": Y,
        "IDStateMtch": Y,
        "SSNMtch": Y,
        "DOBMtch": Y,
        "HmPhoneMtch": Y,
        "WkPhoneMtch": Y,
        "OverallMtchScore": 95.0
    }
    
    result = validate_matches(data)
    assert result.valid is False
    assert result.error_type == ValidationErrorType.INVALID_VALUE
    assert result.field_name == "NameMtch"
    
    # Test with empty values
    data = {
        "NameMtch": "",
        "BusNameMtch": Y,
        "AddressMtch": Y,
        "CityMtch": Y,
        "StateMtch": Y,
        "ZipMtch": Y,
        "IDTypeMtch": Y,
        "IDNoMtch": Y,
        "IDStateMtch": Y,
        "SSNMtch": Y,
        "DOBMtch": Y,
        "HmPhoneMtch": Y,
        "WkPhoneMtch": Y,
        "OverallMtchScore": 95.0
    }
    
    result = validate_matches(data)
    assert result.valid is False
    assert result.error_type == ValidationErrorType.INVALID_VALUE
    assert result.field_name == "NameMtch"
    
    # Test with whitespace values
    data = {
        "NameMtch": " Y ",
        "BusNameMtch": Y,
        "AddressMtch": Y,
        "CityMtch": Y,
        "StateMtch": Y,
        "ZipMtch": Y,
        "IDTypeMtch": Y,
        "IDNoMtch": Y,
        "IDStateMtch": Y,
        "SSNMtch": Y,
        "DOBMtch": Y,
        "HmPhoneMtch": Y,
        "WkPhoneMtch": Y,
        "OverallMtchScore": 95.0
    }
    
    result = validate_matches(data)
    assert result.valid is True
    assert result.error is None
