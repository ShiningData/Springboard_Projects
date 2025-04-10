#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create PAI Address, ID, and Name features

Mapping Name, Address, and ID features into PAI Business Logic Values:
- PAIAddressMtch (AddressMtch, CityMtch, StateMtch, ZipMtch)
- PAIIDMtch (IDTypeMtch, IDNoMtch, IDStateMtch)
- PAINameMtch (NameMtch, BusNameMtch)
"""
__author__ = "Engin Turkmen"
__credits__ = []
__maintainer__ = "Engin Turkmen"
__email__ = "engin.turkmen@pnc.com"
__status__ = "Development"
__version__ = "0.0.1"

from typing import Dict, Any, Optional, Union
import time

# Pre-define constants for optimization
DEFAULT_RETURN = "N"
MISSING_VALUE = "MISSING"
EMPTY_VALUE = ""
Y_VALUE = "Y"
N_VALUE = "N"
U_VALUE = "U"

# Pre-computed address mapping for common combinations
# More limited than the original to improve performance
ADDRESS_MAPPING = {
    # Essential mappings for common combinations
    "YYYY": Y_VALUE,
    "YYY": Y_VALUE,
    "YY": Y_VALUE,
    "Y": Y_VALUE,
    "N": N_VALUE,
    "NN": N_VALUE,
    "NNN": N_VALUE,
    "NNNN": N_VALUE,
    "U": U_VALUE,
    "UU": U_VALUE,
    "UUU": U_VALUE,
    "UUUU": U_VALUE,
    "MISSINGMISSINGMISSINGMISSING": MISSING_VALUE,
    
    # Mixed common cases (optimized for real-world scenarios)
    "YMISSING": Y_VALUE,
    "MISSINGY": Y_VALUE,
    "MISSINGMISSING": MISSING_VALUE,
    "YU": Y_VALUE,
    "UY": Y_VALUE,
    "YN": N_VALUE,
    "NY": N_VALUE,
    "UN": N_VALUE,
    "NU": N_VALUE,
}

# Pre-computed ID mapping - more limited but covers key patterns
ID_MAPPING = {
    "YYY": Y_VALUE,
    "YY": Y_VALUE,
    "Y": Y_VALUE,
    "N": N_VALUE,
    "NN": N_VALUE,
    "NNN": N_VALUE,
    "U": U_VALUE,
    "UU": U_VALUE,
    "UUU": U_VALUE,
    "MISSINGMISSINGMISSING": MISSING_VALUE,
    "YMISSING": Y_VALUE,
    "MISSINGY": Y_VALUE,
}

# Pre-computed name mapping
NAME_MAPPING = {
    "YY": Y_VALUE,
    "Y": Y_VALUE,
    "YMISSING": Y_VALUE,
    "MISSINGY": Y_VALUE,
    "NN": N_VALUE,
    "N": N_VALUE,
    "UU": U_VALUE,
    "U": U_VALUE,
    "MISSINGMISSING": MISSING_VALUE,
    "MISSING": MISSING_VALUE,
}

# Pre-define result dictionary keys for faster access
RESULT_KEYS = ['PAIAddressMtch', 'PAIIDMtch', 'PAINameMtch']

def normalize_input(value: Optional[str]) -> str:
    """
    Normalize input values to handle None and empty strings consistently.
    
    Args:
        value: Input value to normalize
        
    Returns:
        str: Normalized value ("MISSING" for None or empty string)
    """
    if value is None or value == EMPTY_VALUE:
        return MISSING_VALUE
    return value


def mapping_address_match(AddressMtch: Optional[str], CityMtch: Optional[str], 
                         StateMtch: Optional[str], ZipMtch: Optional[str]) -> str:
    """
    Maps a concatenated address matching string to a corresponding value based
    on predefined conditions.
    
    Parameters:
        AddressMtch (str): A match indicator for the address
            ("Y", "N", "C", "U")
        CityMtch (str): A match indicator for the city ("Y", "N", "C", "U")
        StateMtch (str): A match indicator for the state ("Y", "N", "C", "U")
        ZipMtch (str): A match indicator for the zip code ("Y", "N", "C", "U")
            
    Returns:
        str: A mapped value ("Y", "N", "MISSING") corresponding to the
            concatenated address match string.
    """
    # Normalize each input value
    AddressMtch = normalize_input(AddressMtch)
    CityMtch = normalize_input(CityMtch)
    StateMtch = normalize_input(StateMtch)
    ZipMtch = normalize_input(ZipMtch)
    
    # Fast path for common cases
    if AddressMtch == Y_VALUE:
        return Y_VALUE
    elif AddressMtch == N_VALUE:
        return N_VALUE
    elif all(val == MISSING_VALUE for val in (AddressMtch, CityMtch, StateMtch, ZipMtch)):
        return MISSING_VALUE
    
    # Concatenate the values for dictionary lookup
    concatenated_address = AddressMtch + CityMtch + StateMtch + ZipMtch
    
    # Use dictionary lookup with get() to provide a default value
    return ADDRESS_MAPPING.get(concatenated_address, DEFAULT_RETURN)


def mapping_id_match(IDTypeMtch: Optional[str], IDNoMtch: Optional[str], 
                    IDStateMtch: Optional[str]) -> str:
    """
    Maps a concatenated ID matching string to a corresponding value based
    on predefined conditions.
    
    Parameters:
        IDTypeMtch (str): A match indicator for the ID type ("Y", "N", "U")
        IDNoMtch (str): A match indicator for the ID number
            ("Y", "N", "C", "U")
        IDStateMtch (str): A match indicator for the state ("Y", "N", "U")
            
    Returns:
        str: A mapped value ("Y", "N", "MISSING") corresponding to the
            concatenated ID match string.
    """
    # Normalize each input value
    IDTypeMtch = normalize_input(IDTypeMtch)
    IDNoMtch = normalize_input(IDNoMtch)
    IDStateMtch = normalize_input(IDStateMtch)
    
    # Fast path for common cases
    if IDNoMtch == Y_VALUE:
        return Y_VALUE
    elif IDNoMtch == N_VALUE:
        return N_VALUE
    elif all(val == MISSING_VALUE for val in (IDTypeMtch, IDNoMtch, IDStateMtch)):
        return MISSING_VALUE
    
    # Concatenate the values for dictionary lookup
    concatenated_id = IDTypeMtch + IDNoMtch + IDStateMtch
    
    # Use dictionary lookup with get() to provide a default value
    return ID_MAPPING.get(concatenated_id, DEFAULT_RETURN)


def mapping_name_match(NameMtch: Optional[str], BusNameMtch: Optional[str]) -> str:
    """
    Maps a concatenated Name matching string to a corresponding value based
    on predefined conditions.
    
    Parameters:
        NameMtch (str): A match indicator for the Name Match
            ("Y", "N", "C", "U", "MISSING")
        BusNameMtch (str): A match indicator for the Business Name Match
            ("Y", "N", "C", "U", "MISSING")
            
    Returns:
        str: A mapped value ("Y", "N", "U", "MISSING") corresponding to the
            concatenated name match string.
    """
    # Normalize each input value
    NameMtch = normalize_input(NameMtch)
    BusNameMtch = normalize_input(BusNameMtch)
    
    # Fast paths for common cases
    if NameMtch == Y_VALUE:
        return Y_VALUE
    elif NameMtch == N_VALUE:
        return N_VALUE
    elif NameMtch == U_VALUE:
        return U_VALUE
    elif NameMtch == MISSING_VALUE and BusNameMtch == MISSING_VALUE:
        return MISSING_VALUE
    elif NameMtch == MISSING_VALUE and BusNameMtch == Y_VALUE:
        return Y_VALUE
    
    # Concatenate the values for dictionary lookup
    concatenated_name = NameMtch + BusNameMtch
    
    # Use dictionary lookup with get() to provide a default value
    return NAME_MAPPING.get(concatenated_name, DEFAULT_RETURN)


def create_pai_features(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create PAI features from input data.
    
    Args:
        data (dict): Dictionary containing match values
        
    Returns:
        dict: Dictionary with added PAI* features
    """
    # Pre-allocate result dictionary with known keys for faster access
    result = dict(data)
    
    # Map address features - use direct access for known keys
    result['PAIAddressMtch'] = mapping_address_match(
        data.get('AddressMtch'),
        data.get('CityMtch'),
        data.get('StateMtch'),
        data.get('ZipMtch')
    )
    
    # Map ID features - use direct access for known keys
    result['PAIIDMtch'] = mapping_id_match(
        data.get('IDTypeMtch'),
        data.get('IDNoMtch'),
        data.get('IDStateMtch')
    )
    
    # Map name features - use direct access for known keys
    result['PAINameMtch'] = mapping_name_match(
        data.get('NameMtch'),
        data.get('BusNameMtch')
    )
    
    return result


def create_pai_features_optimized(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Optimized version of create_pai_features for real-time inference.
    Uses direct dictionary access and minimizes function call overhead.
    
    Args:
        data (dict): Dictionary containing match values
        
    Returns:
        dict: Dictionary with added PAI* features
    """
    # Pre-allocate result dictionary with known keys for faster access
    result = dict(data)
    
    # Extract values once to avoid repeated dictionary lookups
    address_mtch = data.get('AddressMtch')
    city_mtch = data.get('CityMtch')
    state_mtch = data.get('StateMtch')
    zip_mtch = data.get('ZipMtch')
    
    id_type_mtch = data.get('IDTypeMtch')
    id_no_mtch = data.get('IDNoMtch')
    id_state_mtch = data.get('IDStateMtch')
    
    name_mtch = data.get('NameMtch')
    bus_name_mtch = data.get('BusNameMtch')
    
    # Normalize values once
    address_mtch = normalize_input(address_mtch)
    city_mtch = normalize_input(city_mtch)
    state_mtch = normalize_input(state_mtch)
    zip_mtch = normalize_input(zip_mtch)
    
    id_type_mtch = normalize_input(id_type_mtch)
    id_no_mtch = normalize_input(id_no_mtch)
    id_state_mtch = normalize_input(id_state_mtch)
    
    name_mtch = normalize_input(name_mtch)
    bus_name_mtch = normalize_input(bus_name_mtch)
    
    # Address mapping with fast paths
    if address_mtch == Y_VALUE:
        result['PAIAddressMtch'] = Y_VALUE
    elif address_mtch == N_VALUE:
        result['PAIAddressMtch'] = N_VALUE
    elif all(val == MISSING_VALUE for val in (address_mtch, city_mtch, state_mtch, zip_mtch)):
        result['PAIAddressMtch'] = MISSING_VALUE
    else:
        concatenated_address = address_mtch + city_mtch + state_mtch + zip_mtch
        result['PAIAddressMtch'] = ADDRESS_MAPPING.get(concatenated_address, DEFAULT_RETURN)
    
    # ID mapping with fast paths
    if id_no_mtch == Y_VALUE:
        result['PAIIDMtch'] = Y_VALUE
    elif id_no_mtch == N_VALUE:
        result['PAIIDMtch'] = N_VALUE
    elif all(val == MISSING_VALUE for val in (id_type_mtch, id_no_mtch, id_state_mtch)):
        result['PAIIDMtch'] = MISSING_VALUE
    else:
        concatenated_id = id_type_mtch + id_no_mtch + id_state_mtch
        result['PAIIDMtch'] = ID_MAPPING.get(concatenated_id, DEFAULT_RETURN)
    
    # Name mapping with fast paths
    if name_mtch == Y_VALUE:
        result['PAINameMtch'] = Y_VALUE
    elif name_mtch == N_VALUE:
        result['PAINameMtch'] = N_VALUE
    elif name_mtch == U_VALUE:
        result['PAINameMtch'] = U_VALUE
    elif name_mtch == MISSING_VALUE and bus_name_mtch == MISSING_VALUE:
        result['PAINameMtch'] = MISSING_VALUE
    elif name_mtch == MISSING_VALUE and bus_name_mtch == Y_VALUE:
        result['PAINameMtch'] = Y_VALUE
    else:
        concatenated_name = name_mtch + bus_name_mtch
        result['PAINameMtch'] = NAME_MAPPING.get(concatenated_name, DEFAULT_RETURN)
    
    return result


def test_mapping_performance():
    """Test the performance of mapping functions."""
    import time
    
    # Test data
    test_data = {
        "AddressMtch": "Y",
        "CityMtch": "Y",
        "StateMtch": "Y",
        "ZipMtch": "Y",
        "IDTypeMtch": "Y",
        "IDNoMtch": "Y",
        "IDStateMtch": "Y",
        "NameMtch": "Y",
        "BusNameMtch": "Y",
        "OverallMtchScore": 95
    }
    
    # Test performance
    iterations = 100000
    
    # Test address mapping
    start_time = time.time()
    for _ in range(iterations):
        mapping_address_match("Y", "Y", "Y", "Y")
    address_elapsed = (time.time() - start_time) * 1000000 / iterations  # microseconds
    
    # Test ID mapping
    start_time = time.time()
    for _ in range(iterations):
        mapping_id_match("Y", "Y", "Y")
    id_elapsed = (time.time() - start_time) * 1000000 / iterations  # microseconds
    
    # Test name mapping
    start_time = time.time()
    for _ in range(iterations):
        mapping_name_match("Y", "Y")
    name_elapsed = (time.time() - start_time) * 1000000 / iterations  # microseconds
    
    # Test full feature creation
    start_time = time.time()
    for _ in range(iterations):
        create_pai_features(test_data)
    full_elapsed = (time.time() - start_time) * 1000000 / iterations  # microseconds
    
    # Test optimized feature creation
    start_time = time.time()
    for _ in range(iterations):
        create_pai_features_optimized(test_data)
    optimized_elapsed = (time.time() - start_time) * 1000000 / iterations  # microseconds
    
    print("Performance Test Results:")
    print(f"Address mapping: {address_elapsed:.2f} microseconds")
    print(f"ID mapping: {id_elapsed:.2f} microseconds")
    print(f"Name mapping: {name_elapsed:.2f} microseconds")
    print(f"Full feature creation: {full_elapsed:.2f} microseconds")
    print(f"Optimized feature creation: {optimized_elapsed:.2f} microseconds")
    print(f"Optimization improvement: {(full_elapsed - optimized_elapsed) / full_elapsed * 100:.2f}%")


if __name__ == "__main__":
    # Example data
    example = {
        "AddressMtch": "Y",
        "CityMtch": "Y", 
        "StateMtch": "U",
        "ZipMtch": "Y",
        "IDTypeMtch": "Y",
        "IDNoMtch": "Y",
        "IDStateMtch": "Y",
        "NameMtch": "Y",
        "BusNameMtch": "MISSING",
        "HmPhoneMtch": "Y",
        "WkPhoneMtch": "Y",
        "SSNMtch": "Y",
        "DOBMtch": "Y",
        "OverallMtchScore": 95
    }
    
    # Create PAI features
    result = create_pai_features(example)
    
    # Display results
    print("Input Data:")
    for k, v in example.items():
        print(f"  {k}: {v}")
    
    print("\nPAI Features:")
    print(f"  PAIAddressMtch: {result['PAIAddressMtch']}")
    print(f"  PAIIDMtch: {result['PAIIDMtch']}")
    print(f"  PAINameMtch: {result['PAINameMtch']}")
    
    # Test performance
    test_mapping_performance()
