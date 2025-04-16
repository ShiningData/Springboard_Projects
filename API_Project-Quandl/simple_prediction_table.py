#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for create_pai_mapping.py
"""
import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from create_pai_mapping import (
    normalize_input,
    mapping_address_match,
    mapping_id_match,
    mapping_name_match,
    create_pai_features
)

# Constants for testing
Y_VALUE = "Y"
N_VALUE = "N"
U_VALUE = "U"
MISSING_VALUE = "MISSING"
DEFAULT_RETURN = "N"

# Test normalize_input function
def test_normalize_input():
    """Test the normalize_input function with various inputs"""
    # Test with None
    assert normalize_input(None) == MISSING_VALUE
    
    # Test with empty string
    assert normalize_input("") == MISSING_VALUE
    
    # Test with valid string
    assert normalize_input("Y") == Y_VALUE
    assert normalize_input("N") == N_VALUE
    assert normalize_input("U") == U_VALUE
    
    # Test with whitespace
    assert normalize_input(" Y ") == Y_VALUE
    assert normalize_input(" N ") == N_VALUE
    assert normalize_input(" U ") == U_VALUE
    
    # Test with case
    assert normalize_input("y") == Y_VALUE
    assert normalize_input("n") == N_VALUE
    assert normalize_input("u") == U_VALUE
    
    # Test with invalid values
    assert normalize_input("invalid") == MISSING_VALUE
    assert normalize_input("123") == MISSING_VALUE

# Test mapping_address_match function
def test_mapping_address_match():
    """Test the mapping_address_match function with various inputs"""
    # Test with all Y values
    assert mapping_address_match(Y_VALUE, Y_VALUE, Y_VALUE, Y_VALUE) == Y_VALUE
    
    # Test with all N values
    assert mapping_address_match(N_VALUE, N_VALUE, N_VALUE, N_VALUE) == N_VALUE
    
    # Test with all U values
    assert mapping_address_match(U_VALUE, U_VALUE, U_VALUE, U_VALUE) == U_VALUE
    
    # Test with all MISSING values
    assert mapping_address_match(MISSING_VALUE, MISSING_VALUE, MISSING_VALUE, MISSING_VALUE) == MISSING_VALUE
    
    # Test with None values
    assert mapping_address_match(None, None, None, None) == MISSING_VALUE
    
    # Test with empty values
    assert mapping_address_match("", "", "", "") == MISSING_VALUE
    
    # Test with mixed values
    assert mapping_address_match(Y_VALUE, MISSING_VALUE, U_VALUE, N_VALUE) == N_VALUE  # N takes precedence
    assert mapping_address_match(N_VALUE, Y_VALUE, Y_VALUE, Y_VALUE) == N_VALUE  # N takes precedence
    assert mapping_address_match(Y_VALUE, Y_VALUE, N_VALUE, Y_VALUE) == N_VALUE  # N takes precedence
    
    # Test with None and empty mixed with Y_VALUE and MISSING_VALUE
    assert mapping_address_match(None, Y_VALUE, "", MISSING_VALUE) == N_VALUE  # Mixed values not in ADDRESS_MAPPING return DEFAULT_RETURN (N_VALUE)
    
    # Test with whitespace
    assert mapping_address_match(" Y ", " N ", " U ", " MISSING ") == N_VALUE  # Whitespace is stripped and N takes precedence

# Test mapping_id_match function
def test_mapping_id_match():
    """Test the mapping_id_match function with various inputs"""
    # Test with all Y values
    assert mapping_id_match(Y_VALUE, Y_VALUE, Y_VALUE) == Y_VALUE
    
    # Test with all N values
    assert mapping_id_match(N_VALUE, N_VALUE, N_VALUE) == N_VALUE
    
    # Test with all U values
    assert mapping_id_match(U_VALUE, U_VALUE, U_VALUE) == U_VALUE
    
    # Test with all MISSING values
    assert mapping_id_match(MISSING_VALUE, MISSING_VALUE, MISSING_VALUE) == MISSING_VALUE
    
    # Test with None values
    assert mapping_id_match(None, None, None) == MISSING_VALUE
    
    # Test with empty values
    assert mapping_id_match("", "", "") == MISSING_VALUE
    
    # Test with mixed values
    assert mapping_id_match(Y_VALUE, N_VALUE, U_VALUE) == N_VALUE  # IDNoMtch is N
    assert mapping_id_match(N_VALUE, Y_VALUE, MISSING_VALUE) == Y_VALUE  # IDNoMtch is Y
    assert mapping_id_match(U_VALUE, MISSING_VALUE, Y_VALUE) == MISSING_VALUE  # IDNoMtch is MISSING
    
    # Test with None and empty mixed
    assert mapping_id_match(None, Y_VALUE, "") == Y_VALUE
    assert mapping_id_match("", None, N_VALUE) == N_VALUE
    
    # Test with whitespace
    assert mapping_id_match(" Y ", " N ", " U ") == N_VALUE

# Test mapping_name_match function
def test_mapping_name_match():
    """Test the mapping_name_match function with various inputs"""
    # Test with all Y values
    assert mapping_name_match(Y_VALUE, Y_VALUE) == Y_VALUE
    
    # Test with all N values
    assert mapping_name_match(N_VALUE, N_VALUE) == N_VALUE
    
    # Test with all U values
    assert mapping_name_match(U_VALUE, U_VALUE) == U_VALUE
    
    # Test with all MISSING values
    assert mapping_name_match(MISSING_VALUE, MISSING_VALUE) == MISSING_VALUE
    
    # Test with None values
    assert mapping_name_match(None, None) == MISSING_VALUE
    
    # Test with empty values
    assert mapping_name_match("", "") == MISSING_VALUE
    
    # Test with mixed values
    assert mapping_name_match(Y_VALUE, N_VALUE) == Y_VALUE  # NameMtch is Y
    assert mapping_name_match(N_VALUE, Y_VALUE) == N_VALUE  # NameMtch is N
    assert mapping_name_match(U_VALUE, Y_VALUE) == U_VALUE  # NameMtch is U
    assert mapping_name_match(MISSING_VALUE, Y_VALUE) == Y_VALUE  # NameMtch is MISSING, BusNameMtch is Y
    assert mapping_name_match(MISSING_VALUE, MISSING_VALUE) == MISSING_VALUE  # Both MISSING
    
    # Test with None and empty mixed
    assert mapping_name_match(None, Y_VALUE) == Y_VALUE
    assert mapping_name_match("", None) == MISSING_VALUE
    
    # Test with whitespace
    assert mapping_name_match(" Y ", " N ") == Y_VALUE

# Test create_pai_features function
def test_create_pai_features():
    """Test the create_pai_features function with various inputs."""
    # Test with all Y values
    data = {
        "NameMtch": Y_VALUE,
        "BusNameMtch": Y_VALUE,
        "AddressMtch": Y_VALUE,
        "CityMtch": Y_VALUE,
        "StateMtch": Y_VALUE,
        "ZipMtch": Y_VALUE,
        "IDTypeMtch": Y_VALUE,
        "IDNoMtch": Y_VALUE,
        "IDStateMtch": Y_VALUE
    }
    result = create_pai_features(data)
    assert result["PAINameMtch"] == Y_VALUE
    assert result["PAIAddressMtch"] == Y_VALUE
    assert result["PAIIDMtch"] == Y_VALUE

    # Test with all N values
    data = {
        "NameMtch": N_VALUE,
        "BusNameMtch": N_VALUE,
        "AddressMtch": N_VALUE,
        "CityMtch": N_VALUE,
        "StateMtch": N_VALUE,
        "ZipMtch": N_VALUE,
        "IDTypeMtch": N_VALUE,
        "IDNoMtch": N_VALUE,
        "IDStateMtch": N_VALUE
    }
    result = create_pai_features(data)
    assert result["PAINameMtch"] == N_VALUE
    assert result["PAIAddressMtch"] == N_VALUE
    assert result["PAIIDMtch"] == N_VALUE

    # Test with mixed values
    data = {
        "NameMtch": Y_VALUE,
        "BusNameMtch": N_VALUE,
        "AddressMtch": Y_VALUE,
        "CityMtch": N_VALUE,
        "StateMtch": Y_VALUE,
        "ZipMtch": N_VALUE,
        "IDTypeMtch": Y_VALUE,
        "IDNoMtch": N_VALUE,
        "IDStateMtch": Y_VALUE
    }
    result = create_pai_features(data)
    assert result["PAINameMtch"] == Y_VALUE  # Y takes precedence for name match
    assert result["PAIAddressMtch"] == N_VALUE  # N takes precedence for address match
    assert result["PAIIDMtch"] == N_VALUE  # N takes precedence for ID match

    # Test with missing values
    data = {
        "NameMtch": MISSING_VALUE,
        "BusNameMtch": MISSING_VALUE,
        "AddressMtch": MISSING_VALUE,
        "CityMtch": MISSING_VALUE,
        "StateMtch": MISSING_VALUE,
        "ZipMtch": MISSING_VALUE,
        "IDTypeMtch": MISSING_VALUE,
        "IDNoMtch": MISSING_VALUE,
        "IDStateMtch": MISSING_VALUE
    }
    result = create_pai_features(data)
    assert result["PAINameMtch"] == MISSING_VALUE
    assert result["PAIAddressMtch"] == MISSING_VALUE
    assert result["PAIIDMtch"] == MISSING_VALUE
    
    # Test with missing fields
    data = {
        "NameMtch": Y_VALUE,
        "BusNameMtch": Y_VALUE,
        "AddressMtch": Y_VALUE,
        "CityMtch": Y_VALUE,
        "StateMtch": Y_VALUE,
        "ZipMtch": Y_VALUE,
        # Missing IDTypeMtch, IDNoMtch, IDStateMtch
    }
    result = create_pai_features(data)
    assert result["PAINameMtch"] == Y_VALUE
    assert result["PAIAddressMtch"] == Y_VALUE
    assert result["PAIIDMtch"] == MISSING_VALUE  # Missing fields default to MISSING_VALUE
    
    # Test with additional fields
    data = {
        "NameMtch": Y_VALUE,
        "BusNameMtch": Y_VALUE,
        "AddressMtch": Y_VALUE,
        "CityMtch": Y_VALUE,
        "StateMtch": Y_VALUE,
        "ZipMtch": Y_VALUE,
        "IDTypeMtch": Y_VALUE,
        "IDNoMtch": Y_VALUE,
        "IDStateMtch": Y_VALUE,
        "AdditionalField": "SomeValue"  # Additional field should be preserved
    }
    result = create_pai_features(data)
    assert result["PAINameMtch"] == Y_VALUE
    assert result["PAIAddressMtch"] == Y_VALUE
    assert result["PAIIDMtch"] == Y_VALUE
    assert result["AdditionalField"] == "SomeValue"  # Additional field should be preserved 
