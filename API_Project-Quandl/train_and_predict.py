#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pydantic Data Validation

Account Authentication Model Class.
"""
__author__ = "Engin Turkmen"
__credits__ = []
__maintainer__ = "Engin Turkmen"
__email__ = "engin.turkmen@pnc.com"
__status__ = "Development"
__version__ = "0.0.1"

# Import Pydantic with version compatibility
try:
    # Try Pydantic v2 imports first
    from pydantic import BaseModel, Field, field_validator, ConfigDict
except ImportError:
    try:
        # Fall back to Pydantic v1 imports
        from pydantic import BaseModel, Field, validator, ConfigDict
        # Create an alias for compatibility
        field_validator = validator
    except ImportError:
        # If both fail, try the most basic import
        from pydantic import BaseModel, Field, validator
        # Create aliases for compatibility
        field_validator = validator
        ConfigDict = dict

from typing import Optional, Dict, Any, Set, FrozenSet, ClassVar, Literal, Union
from enum import Enum
from functools import lru_cache
import threading
import time
import json
import hashlib
from cachetools import LRUCache


# Define allowed values as enums for better validation performance
class MatchStatus(str, Enum):
    Y = "Y"
    N = "N"
    C = "C"
    U = "U"
    MISSING = "MISSING"


# Thread-safe cache for model instances
_model_cache = LRUCache(maxsize=10000)
_cache_lock = threading.Lock()


class AccAuthModel(BaseModel):
    """
    A Pydantic model representing the input data required for bank account
    authentication prediction.
    
    Attributes:
        NameMtch (Optional[str]): Match status for Name.
            Defaults to "MISSING".
        BusNameMtch (Optional[str]): Match status for Business Name.
            Defaults to "MISSING".
        SSNMtch (Optional[str]): Match status for SSN.
            Defaults to "MISSING".
        DOBMtch (Optional[str]): Match status for Date of Birth.
            Defaults to "MISSING".
        AddressMtch (Optional[str]): Match status for Address.
            Defaults to "MISSING".
        CityMtch (Optional[str]): Match status for City.
            Defaults to "U".
        StateMtch (Optional[str]): Match status for State.
            Defaults to "U".
        ZipMtch (Optional[str]): Match status for Zip Code.
            Defaults to "U".
        HmPhoneMtch (Optional[str]): Match status for Home Phone.
            Defaults to "MISSING".
        WkPhoneMtch (Optional[str]): Match status for Work Phone.
            Defaults to "MISSING".
        IDTypeMtch (Optional[str]): Match status for ID Type.
            Defaults to "MISSING".
        IDNoMtch (Optional[str]): Match status for ID Number.
            Defaults to "MISSING".
        IDStateMtch (Optional[str]): Match status for ID State.
            Defaults to "MISSING".
        OverallMtchScore (int): The overall match score for the customer.
    """
    # Use ClassVar for class-level constants to avoid instance overhead
    _conditional_match_fields: ClassVar[FrozenSet[str]] = frozenset({
        'NameMtch', 'BusNameMtch', 'AddressMtch', 'CityMtch', 'ZipMtch',
        'HmPhoneMtch', 'WkPhoneMtch', 'SSNMtch', 'DOBMtch', 'IDNoMtch'
    })
    
    _yn_only_fields: ClassVar[FrozenSet[str]] = frozenset({
        'StateMtch', 'IDTypeMtch', 'IDStateMtch'
    })
    
    # Define valid values for each field type as frozensets for O(1) lookup
    _valid_conditional: ClassVar[FrozenSet[str]] = frozenset({'Y', 'N', 'C', 'U', 'MISSING'})
    _valid_yn: ClassVar[FrozenSet[str]] = frozenset({'Y', 'N', 'U', 'MISSING'})
    
    # Define field defaults using Field for better performance
    NameMtch: Optional[str] = Field(default="MISSING", description="Match status for Name.")
    BusNameMtch: Optional[str] = Field(default="MISSING", description="Match status for Business Name.")
    SSNMtch: Optional[str] = Field(default="MISSING", description="Match status for SSN.")
    DOBMtch: Optional[str] = Field(default="MISSING", description="Match status for Date of Birth.")
    AddressMtch: Optional[str] = Field(default="U", description="Match status for Address.")
    CityMtch: Optional[str] = Field(default="U", description="Match status for City.")
    StateMtch: Optional[str] = Field(default="U", description="Match status for State.")
    ZipMtch: Optional[str] = Field(default="U", description="Match status for Zip Code.")
    HmPhoneMtch: Optional[str] = Field(default="MISSING", description="Match status for Home Phone.")
    WkPhoneMtch: Optional[str] = Field(default="MISSING", description="Match status for Work Phone.")
    IDTypeMtch: Optional[str] = Field(default="MISSING", description="Match status for ID Type.")
    IDNoMtch: Optional[str] = Field(default="MISSING", description="Match status for ID Number.")
    IDStateMtch: Optional[str] = Field(default="MISSING", description="Match status for ID State.")
    OverallMtchScore: int = Field(..., description="The overall match score for the customer.")
    
    # Use model_config for better performance in Pydantic v2
    # For Pydantic v1 compatibility, we'll use a try-except block
    try:
        model_config = ConfigDict(
            json_schema_extra={
                "example": {
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
                    "OverallMtchScore": 100
                }
            },
            validate_assignment=True,
            extra="forbid",
            # Enable frozen mode for better performance
            frozen=True,
            # Use arbitrary_types_allowed for better performance
            arbitrary_types_allowed=True
        )
    except (NameError, TypeError):
        # Fall back to Pydantic v1 config
        class Config:
            schema_extra = {
                "example": {
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
                    "OverallMtchScore": 100
                }
            }
            validate_assignment = True
            extra = "forbid"
    
    @field_validator('OverallMtchScore')
    @classmethod
    def validate_score(cls, v):
        # Early return for valid integers
        if isinstance(v, int) and 0 <= v <= 100:
            return v
            
        # Handle string inputs
        if isinstance(v, str):
            try:
                score = int(v)
                if 0 <= score <= 100:
                    return score
            except ValueError:
                pass
                
        raise ValueError("OverallMtchScore must be an integer between 0 and 100")
    
    @field_validator('*', mode='before')
    @classmethod
    def validate_fields(cls, v, info):
        # Skip validation for None values (will use default)
        if v is None:
            return v
            
        # Convert to string for consistent handling
        if not isinstance(v, str):
            v = str(v).strip().upper()
            
        # Validate conditional match fields
        if info.field_name in cls._conditional_match_fields:
            if v not in cls._valid_conditional:
                raise ValueError(f"Invalid value for {info.field_name}: {v}. Must be one of {cls._valid_conditional}")
                
        # Validate Y/N only fields
        elif info.field_name in cls._yn_only_fields:
            if v not in cls._valid_yn:
                raise ValueError(f"Invalid value for {info.field_name}: {v}. Must be one of {cls._valid_yn}")
                
        return v
    
    @classmethod
    @lru_cache(maxsize=1024)
    def _generate_cache_key(cls, **data) -> str:
        """
        Generate a cache key from the input data.
        
        Args:
            **data: Keyword arguments for model fields
            
        Returns:
            str: A hash of the data for caching
        """
        # Sort keys for consistent hashing
        sorted_data = {k: data[k] for k in sorted(data.keys())}
        # Convert to JSON and hash
        data_str = json.dumps(sorted_data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    @classmethod
    def create(cls, **data):
        """
        Create a new instance with caching for performance.
        
        Args:
            **data: Keyword arguments for model fields
            
        Returns:
            AccAuthModel: A new model instance
        """
        # Generate a cache key from the data
        cache_key = cls._generate_cache_key(**data)
        
        # Check if instance is in cache
        with _cache_lock:
            if cache_key in _model_cache:
                return _model_cache[cache_key]
            
            # Create new instance and cache it
            instance = cls(**data)
            _model_cache[cache_key] = instance
            return instance
    
    @staticmethod
    def clear_cache() -> None:
        """Clear the model cache."""
        with _cache_lock:
            _model_cache.clear()
            AccAuthModel._generate_cache_key.cache_clear()
    
    @staticmethod
    def get_cache_stats() -> Dict[str, Any]:
        """
        Get statistics about the model cache.
        
        Returns:
            Dict containing cache statistics
        """
        with _cache_lock:
            return {
                "model_cache_size": len(_model_cache),
                "cache_key_hits": AccAuthModel._generate_cache_key.cache_info().hits,
                "cache_key_misses": AccAuthModel._generate_cache_key.cache_info().misses
            }
    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """
        Override model_dump for better performance.
        
        Args:
            **kwargs: Additional arguments for model_dump
            
        Returns:
            Dict[str, Any]: Dictionary representation of the model
        """
        # Use a faster approach for simple models
        return {
            "NameMtch": self.NameMtch,
            "BusNameMtch": self.BusNameMtch,
            "SSNMtch": self.SSNMtch,
            "DOBMtch": self.DOBMtch,
            "AddressMtch": self.AddressMtch,
            "CityMtch": self.CityMtch,
            "StateMtch": self.StateMtch,
            "ZipMtch": self.ZipMtch,
            "HmPhoneMtch": self.HmPhoneMtch,
            "WkPhoneMtch": self.WkPhoneMtch,
            "IDTypeMtch": self.IDTypeMtch,
            "IDNoMtch": self.IDNoMtch,
            "IDStateMtch": self.IDStateMtch,
            "OverallMtchScore": self.OverallMtchScore
        }


# Alias for backward compatibility
acc_auth_model = AccAuthModel


# Example usage
if __name__ == "__main__":
    import time
    
    # Test data
    test_data = {
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
        "OverallMtchScore": 100
    }
    
    # Performance test
    iterations = 10000
    start_time = time.time()
    
    for _ in range(iterations):
        model = acc_auth_model(**test_data)
        dict_data = model.model_dump()
    
    elapsed = (time.time() - start_time) * 1000 / iterations
    
    print(f"Average processing time: {elapsed:.3f}ms per model ({iterations} iterations)")
    
    # Test with cached creation
    start_time = time.time()
    
    for _ in range(iterations):
        model = acc_auth_model.create(**test_data)
        dict_data = model.model_dump()
    
    cached_elapsed = (time.time() - start_time) * 1000 / iterations
    
    print(f"Average processing time with caching: {cached_elapsed:.3f}ms per model ({iterations} iterations)")
    print(f"Speedup from caching: {elapsed/cached_elapsed:.2f}x")
    
    # Show cache statistics
    cache_stats = acc_auth_model.get_cache_stats()
    print("\nCache statistics:")
    print(f"  Model cache size: {cache_stats['model_cache_size']}")
    print(f"  Cache key hits: {cache_stats['cache_key_hits']}")
    print(f"  Cache key misses: {cache_stats['cache_key_misses']}")
    
    # Show example model
    model = acc_auth_model(**test_data)
    print("\nModel instance created:")
    print(f"NameMtch: {model.NameMtch}")
    print(f"AddressMtch: {model.AddressMtch}")
    print(f"OverallMtchScore: {model.OverallMtchScore}")
    
    # Test with minimal data (using defaults)
    minimal_data = {
        "OverallMtchScore": 95
    }
    
    minimal_model = acc_auth_model(**minimal_data)
    print("\nMinimal model (using defaults):")
    print(f"NameMtch: {minimal_model.NameMtch}")
    print(f"AddressMtch: {minimal_model.AddressMtch}")
    print(f"OverallMtchScore: {minimal_model.OverallMtchScore}")
    
    # Validation test
    try:
        invalid_data = {
            "NameMtch": "INVALID",
            "OverallMtchScore": 95
        }
        invalid_model = acc_auth_model(**invalid_data)
    except ValueError as e:
        print(f"\nValidation error (expected): {e}")
    
    # Clear cache
    acc_auth_model.clear_cache()
    print("\nCache cleared")
