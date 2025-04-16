#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for rule_base_model.py
"""
import pytest
from rule_engine.rule_base_model import (
    CRCCode,
    check_threshold_conditions,
    check_perfect_match,
    count_mismatches,
    handle_single_mismatch,
    handle_multiple_mismatches,
    determine_result_code,
    UPPER_THRESHOLD,
    LOWER_THRESHOLD,
    C_N_VALUES,
    MISSING_VALUES
)

# Test check_threshold_conditions function
def test_check_threshold_conditions():
    """Test the check_threshold_conditions function with various inputs"""
    # Test with missing values
    for missing in MISSING_VALUES:
        assert check_threshold_conditions(missing, 95.0) == CRCCode.INCONCLUSIVE
    
    # Test with score below lower threshold
    assert check_threshold_conditions("Y", LOWER_THRESHOLD - 1) == CRCCode.DECLINE
    assert check_threshold_conditions("N", LOWER_THRESHOLD - 1) == CRCCode.DECLINE
    assert check_threshold_conditions("U", LOWER_THRESHOLD - 1) == CRCCode.DECLINE
    
    # Test with score above upper threshold
    assert check_threshold_conditions("Y", UPPER_THRESHOLD + 1) == CRCCode.PASS
    assert check_threshold_conditions("N", UPPER_THRESHOLD + 1) == CRCCode.WARNING_NAME
    assert check_threshold_conditions("U", UPPER_THRESHOLD + 1) == CRCCode.INCONCLUSIVE
    
    # Test with score between thresholds
    assert check_threshold_conditions("Y", (UPPER_THRESHOLD + LOWER_THRESHOLD) / 2) is None
    assert check_threshold_conditions("N", (UPPER_THRESHOLD + LOWER_THRESHOLD) / 2) is None
    assert check_threshold_conditions("U", (UPPER_THRESHOLD + LOWER_THRESHOLD) / 2) is None
    
    # Test with exact threshold values
    assert check_threshold_conditions("Y", UPPER_THRESHOLD) == CRCCode.PASS
    assert check_threshold_conditions("N", UPPER_THRESHOLD) == CRCCode.WARNING_NAME
    assert check_threshold_conditions("U", UPPER_THRESHOLD) == CRCCode.INCONCLUSIVE
    
    assert check_threshold_conditions("Y", LOWER_THRESHOLD) is None
    assert check_threshold_conditions("N", LOWER_THRESHOLD) is None
    assert check_threshold_conditions("U", LOWER_THRESHOLD) is None

# Test check_perfect_match function
def test_check_perfect_match():
    """Test the check_perfect_match function with various inputs"""
    # Test with perfect match (Y and no C/N values)
    assert check_perfect_match("Y", ("Y", "Y", "Y", "Y", "Y", "Y")) == CRCCode.PASS
    
    # Test with N in pai_name
    assert check_perfect_match("N", ("Y", "Y", "Y", "Y", "Y", "Y")) is None
    
    # Test with U in pai_name
    assert check_perfect_match("U", ("Y", "Y", "Y", "Y", "Y", "Y")) is None
    
    # Test with C in fields
    assert check_perfect_match("Y", ("Y", "C", "Y", "Y", "Y", "Y")) is None
    
    # Test with N in fields
    assert check_perfect_match("Y", ("Y", "Y", "N", "Y", "Y", "Y")) is None
    
    # Test with missing values
    for missing in MISSING_VALUES:
        assert check_perfect_match("Y", (missing, "Y", "Y", "Y", "Y", "Y")) is None
        assert check_perfect_match(missing, ("Y", "Y", "Y", "Y", "Y", "Y")) is None

# Test count_mismatches function
def test_count_mismatches():
    """Test the count_mismatches function with various inputs"""
    # Test with no mismatches
    primary = ("Y", "Y", "Y")
    secondary = ("Y", "Y", "Y", "Y")
    primary_mismatches, secondary_mismatches, total_mismatches = count_mismatches(primary, secondary)
    assert primary_mismatches == 0
    assert secondary_mismatches == 0
    assert total_mismatches == 0
    
    # Test with primary mismatches only
    primary = ("Y", "C", "N")
    secondary = ("Y", "Y", "Y", "Y")
    primary_mismatches, secondary_mismatches, total_mismatches = count_mismatches(primary, secondary)
    assert primary_mismatches == 2
    assert secondary_mismatches == 0
    assert total_mismatches == 2
    
    # Test with secondary mismatches only
    primary = ("Y", "Y", "Y")
    secondary = ("Y", "C", "N", "Y")
    primary_mismatches, secondary_mismatches, total_mismatches = count_mismatches(primary, secondary)
    assert primary_mismatches == 0
    assert secondary_mismatches == 2
    assert total_mismatches == 2
    
    # Test with both primary and secondary mismatches
    primary = ("Y", "C", "N")
    secondary = ("Y", "C", "N", "Y")
    primary_mismatches, secondary_mismatches, total_mismatches = count_mismatches(primary, secondary)
    assert primary_mismatches == 2
    assert secondary_mismatches == 2
    assert total_mismatches == 4
    
    # Test with missing values
    primary = ("Y", "MISSING", "N")
    secondary = ("Y", "C", "N/A", "Y")
    primary_mismatches, secondary_mismatches, total_mismatches = count_mismatches(primary, secondary)
    assert primary_mismatches == 1  # Only N is counted as mismatch
    assert secondary_mismatches == 2  # C and N are counted as mismatches
    assert total_mismatches == 3

# Test handle_single_mismatch function
def test_handle_single_mismatch():
    """Test the handle_single_mismatch function with various inputs"""
    # Test with address mismatch
    assert handle_single_mismatch("C", "Y", "Y", "Y", "Y", "Y", "Y") == CRCCode.CAUTION_ADDRESS
    assert handle_single_mismatch("N", "Y", "Y", "Y", "Y", "Y", "Y") == CRCCode.CAUTION_ADDRESS
    
    # Test with phone mismatch (home)
    assert handle_single_mismatch("Y", "C", "Y", "Y", "Y", "Y", "Y") == CRCCode.CAUTION_PHONE
    assert handle_single_mismatch("Y", "N", "Y", "Y", "Y", "Y", "Y") == CRCCode.CAUTION_PHONE
    
    # Test with phone mismatch (work)
    assert handle_single_mismatch("Y", "Y", "C", "Y", "Y", "Y", "Y") == CRCCode.CAUTION_PHONE
    assert handle_single_mismatch("Y", "Y", "N", "Y", "Y", "Y", "Y") == CRCCode.CAUTION_PHONE
    
    # Test with ID mismatch
    assert handle_single_mismatch("Y", "Y", "Y", "C", "Y", "Y", "Y") == CRCCode.CAUTION_ID
    assert handle_single_mismatch("Y", "Y", "Y", "N", "Y", "Y", "Y") == CRCCode.CAUTION_ID
    
    # Test with name mismatch
    assert handle_single_mismatch("Y", "Y", "Y", "Y", "C", "Y", "Y") == CRCCode.WARNING_NAME
    assert handle_single_mismatch("Y", "Y", "Y", "Y", "N", "Y", "Y") == CRCCode.WARNING_NAME
    
    # Test with SSN mismatch
    assert handle_single_mismatch("Y", "Y", "Y", "Y", "Y", "C", "Y") == CRCCode.WARNING_TAX_ID
    assert handle_single_mismatch("Y", "Y", "Y", "Y", "Y", "N", "Y") == CRCCode.WARNING_TAX_ID
    
    # Test with DOB mismatch
    assert handle_single_mismatch("Y", "Y", "Y", "Y", "Y", "Y", "C") == CRCCode.WARNING_DOB
    assert handle_single_mismatch("Y", "Y", "Y", "Y", "Y", "Y", "N") == CRCCode.WARNING_DOB
    
    # Test with no mismatch
    assert handle_single_mismatch("Y", "Y", "Y", "Y", "Y", "Y", "Y") is None
    
    # Test with missing values
    for missing in MISSING_VALUES:
        assert handle_single_mismatch(missing, "Y", "Y", "Y", "Y", "Y", "Y") == CRCCode.CAUTION_ADDRESS
        assert handle_single_mismatch("Y", missing, "Y", "Y", "Y", "Y", "Y") == CRCCode.CAUTION_PHONE
        assert handle_single_mismatch("Y", "Y", missing, "Y", "Y", "Y", "Y") == CRCCode.CAUTION_PHONE
        assert handle_single_mismatch("Y", "Y", "Y", missing, "Y", "Y", "Y") == CRCCode.CAUTION_ID
        assert handle_single_mismatch("Y", "Y", "Y", "Y", missing, "Y", "Y") == CRCCode.WARNING_NAME
        assert handle_single_mismatch("Y", "Y", "Y", "Y", "Y", missing, "Y") == CRCCode.WARNING_TAX_ID
        assert handle_single_mismatch("Y", "Y", "Y", "Y", "Y", "Y", missing) == CRCCode.WARNING_DOB

# Test handle_multiple_mismatches function
def test_handle_multiple_mismatches():
    """Test the handle_multiple_mismatches function with various inputs"""
    # Test with one primary mismatch and one secondary mismatch
    assert handle_multiple_mismatches(1, 1) == CRCCode.WARNING_MULTIPLE
    
    # Test with one primary mismatch and multiple secondary mismatches
    assert handle_multiple_mismatches(1, 2) == CRCCode.WARNING_MULTIPLE
    assert handle_multiple_mismatches(1, 3) == CRCCode.WARNING_MULTIPLE
    assert handle_multiple_mismatches(1, 4) == CRCCode.WARNING_MULTIPLE
    
    # Test with no primary mismatches and multiple secondary mismatches
    assert handle_multiple_mismatches(0, 2) == CRCCode.WARNING_MULTIPLE
    assert handle_multiple_mismatches(0, 3) == CRCCode.WARNING_MULTIPLE
    assert handle_multiple_mismatches(0, 4) == CRCCode.WARNING_MULTIPLE
    
    # Test with multiple primary mismatches
    assert handle_multiple_mismatches(2, 0) == CRCCode.DECLINE
    assert handle_multiple_mismatches(2, 1) == CRCCode.DECLINE
    assert handle_multiple_mismatches(3, 0) == CRCCode.DECLINE
    assert handle_multiple_mismatches(3, 1) == CRCCode.DECLINE
    
    # Test with no mismatches
    assert handle_multiple_mismatches(0, 0) is None
    
    # Test with one primary mismatch and no secondary mismatches
    assert handle_multiple_mismatches(1, 0) is None
    
    # Test with no primary mismatches and one secondary mismatch
    assert handle_multiple_mismatches(0, 1) is None

# Test determine_result_code function
def test_determine_result_code():
    """Test the determine_result_code function with various inputs"""
    # Test with perfect match
    data = {
        "PAINameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": 95.0
    }
    assert determine_result_code(data) == CRCCode.PASS
    
    # Test with score above upper threshold and Y name match
    data = {
        "PAINameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": UPPER_THRESHOLD + 1
    }
    assert determine_result_code(data) == CRCCode.PASS
    
    # Test with score above upper threshold and N name match
    data = {
        "PAINameMtch": "N",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": UPPER_THRESHOLD + 1
    }
    assert determine_result_code(data) == CRCCode.WARNING_NAME
    
    # Test with score above upper threshold and U name match
    data = {
        "PAINameMtch": "U",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": UPPER_THRESHOLD + 1
    }
    assert determine_result_code(data) == CRCCode.INCONCLUSIVE
    
    # Test with score below lower threshold
    data = {
        "PAINameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": LOWER_THRESHOLD - 1
    }
    assert determine_result_code(data) == CRCCode.DECLINE
    
    # Test with missing name match
    data = {
        "PAINameMtch": "MISSING",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": 95.0
    }
    assert determine_result_code(data) == CRCCode.INCONCLUSIVE
    
    # Test with single address mismatch
    data = {
        "PAINameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "C",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": 85.0
    }
    assert determine_result_code(data) == CRCCode.CAUTION_ADDRESS
    
    # Test with single phone mismatch
    data = {
        "PAINameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "C",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": 85.0
    }
    assert determine_result_code(data) == CRCCode.CAUTION_PHONE
    
    # Test with single ID mismatch
    data = {
        "PAINameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "C",
        "OverallMtchScore": 85.0
    }
    assert determine_result_code(data) == CRCCode.CAUTION_ID
    
    # Test with single name mismatch
    data = {
        "PAINameMtch": "C",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": 85.0
    }
    assert determine_result_code(data) == CRCCode.WARNING_NAME
    
    # Test with single SSN mismatch
    data = {
        "PAINameMtch": "Y",
        "SSNMtch": "C",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": 85.0
    }
    assert determine_result_code(data) == CRCCode.WARNING_TAX_ID
    
    # Test with single DOB mismatch
    data = {
        "PAINameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "C",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": 85.0
    }
    assert determine_result_code(data) == CRCCode.WARNING_DOB
    
    # Test with one primary mismatch and one secondary mismatch
    data = {
        "PAINameMtch": "C",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "C",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": 85.0
    }
    assert determine_result_code(data) == CRCCode.WARNING_MULTIPLE
    
    # Test with multiple primary mismatches
    data = {
        "PAINameMtch": "C",
        "SSNMtch": "C",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y",
        "OverallMtchScore": 85.0
    }
    assert determine_result_code(data) == CRCCode.DECLINE
    
    # Test with missing fields
    data = {
        "PAINameMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "PAIAddressMtch": "Y",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "PAIIDMtch": "Y"
    }
    assert determine_result_code(data) == CRCCode.NO_MATCH
    
    # Test with empty data
    data = {}
    assert determine_result_code(data) == CRCCode.NO_MATCH 
