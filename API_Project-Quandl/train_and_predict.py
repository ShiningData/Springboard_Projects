#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuration Module

Contains application configuration settings.
"""
import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("acc_auth_api")

# API Configuration
API_TITLE = "Account Authentication API"
API_DESCRIPTION = "API for predicting account authentication result codes"
API_VERSION = "0.0.1"

# CORS Configuration
CORS_ORIGINS: List[str] = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# GZip Configuration
GZIP_MIN_SIZE = 1000

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

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000
LOG_LEVEL = "info"
WORKERS = 4
RELOAD = False  # Disable in production 
