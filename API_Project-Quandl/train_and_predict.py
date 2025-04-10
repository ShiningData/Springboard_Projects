#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create Counterparty Result Codes

Translate business logic via mapping given input into CRC response code.

There are 10 CRC response codes as presented below:
* CRC1000: Pass - Bank account authentication passed
* CRC2100: Caution - Address did not match bank account authentication data
* CRC2200: Caution - Phone number did not match bank account authentication data
* CRC2300: Caution - ID did not match bank account authentication data
* CRC3100: Warning - Name did not match bank account authentication data
* CRC3200: Warning - Tax ID did not match bank account authentication data
* CRC3300: Warning - Date of birth did not match bank account authentication data
* CRC3900: Warning - Multiple data points did not match bank account authentication data
* CRC4000: Decline - Bank account authentication failed
* CRC0000: Inconclusive - No reported bank account authentication data
"""
import pathlib
import configparser
import os
from typing import Dict, Union, FrozenSet, Tuple
from enum import Enum

# Load configuration
config = configparser.ConfigParser()


# Get threshold values from config
UPPER_THRESHOLD = 91
LOWER_THRESHOLD = 31

# Pre-define constants for optimization
C_N_VALUES: FrozenSet[str] = frozenset(['C', 'N'])
MISSING_VALUES: FrozenSet[str] = frozenset(['MISSING', 'N/A'])

# Define CRC codes as enum for better performance and type safety
class CRCCode(str, Enum):
    PASS = "CRC1000"
    CAUTION_ADDRESS = "CRC2100"
    CAUTION_PHONE = "CRC2200"
    CAUTION_ID = "CRC2300"
    WARNING_NAME = "CRC3100"
    WARNING_TAX_ID = "CRC3200"
    WARNING_DOB = "CRC3300"
    WARNING_MULTIPLE = "CRC3900"
    DECLINE = "CRC4000"
    INCONCLUSIVE = "CRC0000"
    NO_MATCH = "NO_MATCH"


def check_threshold_conditions(pai_name: str, score: float) -> Union[str, None]:
    """
    Check if the result can be determined based on threshold conditions.
    
    Args:
        pai_name: The PAI name match value
        score: The overall match score
        
    Returns:
        CRC code if determined by thresholds, None otherwise
    """
    # Check for inconclusive first (most restrictive)
    if pai_name in MISSING_VALUES:
        return CRCCode.INCONCLUSIVE
    
    # Check score thresholds
    if score < LOWER_THRESHOLD:
        return CRCCode.DECLINE
        
    if score > UPPER_THRESHOLD:
        if pai_name == "Y":
            return CRCCode.PASS
        if pai_name == "N":
            return CRCCode.WARNING_NAME
        return CRCCode.INCONCLUSIVE
    
    return None


def check_perfect_match(pai_name: str, fields: Tuple[str, ...]) -> Union[str, None]:
    """
    Check if there's a perfect match based on the PAI name and other fields.
    
    Args:
        pai_name: The PAI name match value
        fields: Tuple of other field values to check
        
    Returns:
        CRC code if perfect match, None otherwise
    """
    if pai_name == "Y" and not any(field in C_N_VALUES for field in fields):
        return CRCCode.PASS
    
    return None


def count_mismatches(primary_fields: Tuple[str, ...], secondary_fields: Tuple[str, ...]) -> Tuple[int, int, int]:
    """
    Count the number of mismatches in primary and secondary fields.
    
    Args:
        primary_fields: Tuple of primary field values
        secondary_fields: Tuple of secondary field values
        
    Returns:
        Tuple of (primary_mismatches, secondary_mismatches, total_mismatches)
    """
    primary_mismatches = sum(1 for field in primary_fields if field in C_N_VALUES)
    secondary_mismatches = sum(1 for field in secondary_fields if field in C_N_VALUES)
    total_mismatches = primary_mismatches + secondary_mismatches
    
    return primary_mismatches, secondary_mismatches, total_mismatches


def handle_single_mismatch(address: str, hm_phone: str, wk_phone: str, 
                          pai_id: str, pai_name: str, ssn: str, dob: str) -> Union[str, None]:
    """
    Handle the case where there is exactly one mismatch.
    
    Args:
        address: Address match value
        hm_phone: Home phone match value
        wk_phone: Work phone match value
        pai_id: PAI ID match value
        pai_name: PAI name match value
        ssn: SSN match value
        dob: DOB match value
        
    Returns:
        CRC code if single mismatch identified, None otherwise
    """
    if address in C_N_VALUES:
        return CRCCode.CAUTION_ADDRESS
    if hm_phone in C_N_VALUES or wk_phone in C_N_VALUES:
        return CRCCode.CAUTION_PHONE
    if pai_id in C_N_VALUES:
        return CRCCode.CAUTION_ID
    if pai_name in C_N_VALUES:
        return CRCCode.WARNING_NAME
    if ssn in C_N_VALUES:
        return CRCCode.WARNING_TAX_ID
    if dob in C_N_VALUES:
        return CRCCode.WARNING_DOB
    
    return None


def handle_multiple_mismatches(primary_mismatches: int, secondary_mismatches: int) -> Union[str, None]:
    """
    Handle the case where there are multiple mismatches.
    
    Args:
        primary_mismatches: Number of primary field mismatches
        secondary_mismatches: Number of secondary field mismatches
        
    Returns:
        CRC code if multiple mismatches pattern identified, None otherwise
    """
    # All primary fields valid but secondary mismatches exist
    if primary_mismatches == 0 and secondary_mismatches > 0:
        return CRCCode.WARNING_MULTIPLE
        
    # One primary mismatch and any secondary mismatches
    if primary_mismatches == 1 and secondary_mismatches >= 1:
        return CRCCode.WARNING_MULTIPLE
        
    # Multiple secondary mismatches only
    if primary_mismatches == 0 and secondary_mismatches >= 2:
        return CRCCode.WARNING_MULTIPLE
        
    # Multiple primary mismatches
    if primary_mismatches > 1:
        return CRCCode.DECLINE
    
    return None


def determine_result_code(data: Dict[str, Union[str, float]]) -> str:
    """
    Determine the appropriate CRC code based on input data.
    Optimized for single dictionary input with minimal latency.
    
    Args:
        data: Dictionary containing matching fields and scores
            
    Returns:
        str: CRC code based on the rules
    """
    # Extract key fields
    pai_name: str = data.get('PAINameMtch', '')
    score: float = float(data.get('OverallMtchScore', 0))
    
    # Check threshold conditions first (fast path)
    threshold_result = check_threshold_conditions(pai_name, score)
    if threshold_result:
        return threshold_result
    
    # Extract remaining fields
    ssn: str = data.get('SSNMtch', '')
    dob: str = data.get('DOBMtch', '')
    address: str = data.get('PAIAddressMtch', '')
    hm_phone: str = data.get('HmPhoneMtch', '')
    wk_phone: str = data.get('WkPhoneMtch', '')
    pai_id: str = data.get('PAIIDMtch', '')
    
    # Check for perfect match (fast path)
    perfect_match = check_perfect_match(pai_name, (ssn, dob, address, hm_phone, wk_phone, pai_id))
    if perfect_match:
        return perfect_match
    
    # Count mismatches
    primary_fields = (pai_name, ssn, dob)
    secondary_fields = (address, hm_phone, wk_phone, pai_id)
    primary_mismatches, secondary_mismatches, total_mismatches = count_mismatches(primary_fields, secondary_fields)
    
    # Handle single mismatch
    if total_mismatches == 1:
        single_mismatch = handle_single_mismatch(address, hm_phone, wk_phone, pai_id, pai_name, ssn, dob)
        if single_mismatch:
            return single_mismatch
    
    # Handle multiple mismatches
    if total_mismatches > 1:
        multiple_mismatch = handle_multiple_mismatches(primary_mismatches, secondary_mismatches)
        if multiple_mismatch:
            return multiple_mismatch
    
    # Default case
    return CRCCode.NO_MATCH


def main():
    """
    Main function to test the rule engine performance.
    """
    import time
    
    # Example data
    test_cases = [
        {
            'description': "Pass - All Y with high score",
            'data': {
                'PAINameMtch': 'Y', 'PAIIDMtch': 'Y', 'PAIAddressMtch': 'Y',
                'HmPhoneMtch': 'Y', 'WkPhoneMtch': 'Y', 'SSNMtch': 'Y', 'DOBMtch': 'Y',
                'OverallMtchScore': 95
            },
            'expected': "CRC1000"
        },
        {
            'description': "Warning - Name mismatch with high score",
            'data': {
                'PAINameMtch': 'N', 'PAIIDMtch': 'Y', 'PAIAddressMtch': 'Y',
                'HmPhoneMtch': 'Y', 'WkPhoneMtch': 'Y', 'SSNMtch': 'Y', 'DOBMtch': 'Y',
                'OverallMtchScore': 95
            },
            'expected': "CRC3100"
        },
        {
            'description': "Decline - Low score",
            'data': {
                'PAINameMtch': 'Y', 'PAIIDMtch': 'Y', 'PAIAddressMtch': 'Y',
                'HmPhoneMtch': 'Y', 'WkPhoneMtch': 'Y', 'SSNMtch': 'Y', 'DOBMtch': 'Y',
                'OverallMtchScore': 25
            },
            'expected': "CRC4000"
        },
        {
            'description': "Caution - Address mismatch only",
            'data': {
                'PAINameMtch': 'Y', 'PAIIDMtch': 'Y', 'PAIAddressMtch': 'C',
                'HmPhoneMtch': 'Y', 'WkPhoneMtch': 'Y', 'SSNMtch': 'Y', 'DOBMtch': 'Y',
                'OverallMtchScore': 65
            },
            'expected': "CRC2100"
        },
        {
            'description': "Warning - Multiple mismatches",
            'data': {
                'PAINameMtch': 'Y', 'PAIIDMtch': 'N', 'PAIAddressMtch': 'C',
                'HmPhoneMtch': 'Y', 'WkPhoneMtch': 'Y', 'SSNMtch': 'Y', 'DOBMtch': 'Y',
                'OverallMtchScore': 65
            },
            'expected': "CRC3900"
        }
    ]
    
    # Test individual cases with timing
    print("Testing rule engine with various scenarios:")
    print("=" * 60)
    
    for case in test_cases:
        # Run 10000 times to get a better measure of performance
        iterations = 10000
        start_time = time.time()
        
        result = None
        for _ in range(iterations):
            result = determine_result_code(case['data'])
            
        elapsed = (time.time() - start_time) * 1000 / iterations  # average time in milliseconds
        
        print(f"{case['description']}:")
        print(f"  Result={result}, Expected={case['expected']}")
        print(f"  Average time: {elapsed:.6f}ms ({iterations} iterations)")
        print("-" * 60)
        
        assert result == case['expected'], f"Expected {case['expected']} but got {result}"
    
    # Performance benchmark
    print("\nPerformance benchmark:")
    print("=" * 60)
    
    # Mix all test cases
    all_test_data = [case['data'] for case in test_cases]
    total_iterations = 1000000
    iterations_per_case = total_iterations // len(all_test_data)
    
    start_time = time.time()
    for _ in range(iterations_per_case):
        for data in all_test_data:
            determine_result_code(data)
    
    total_calls = iterations_per_case * len(all_test_data)
    elapsed = time.time() - start_time
    
    print(f"Processed {total_calls:,} inputs in {elapsed:.3f} seconds")
    print(f"Average processing time: {(elapsed / total_calls) * 1000:.6f} ms per input")
    print(f"Throughput: {total_calls / elapsed:,.0f} inputs per second")


if __name__ == "__main__":
    main()
