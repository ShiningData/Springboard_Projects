#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main Module for Model Prediction through the FastAPI

Conduct API request for BAA response data, validate the data values,
and apply rule based model to predict the counterparty result code.
"""
__author__ = "Engin Turkmen"
__credits__ = []
__maintainer__ = "Engin Turkmen"
__email__ = "engin.turkmen@pnc.com"
__status__ = "Development"
__version__ = "0.0.1"

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import logging
import os
from datetime import datetime

# Import custom modules
from config import (
    API_TITLE, API_DESCRIPTION, API_VERSION,
    CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS,
    HOST, PORT, LOG_LEVEL, ENVIRONMENT
)
from rule_base_model import determine_result_code

# Define Pydantic models for request/response
class ResultCodeRequest(BaseModel):
    """
    Request model for the get-result-code endpoint.
    """
    NameMtch: str = Field(..., description="Name match value (Y, N, C, MISSING, N/A)")
    BusNameMtch: str = Field(..., description="Business Name match value (Y, N, C, MISSING, N/A)")
    SSNMtch: str = Field(..., description="SSN match value (Y, N, C, MISSING, N/A)")
    DOBMtch: str = Field(..., description="Date of Birth match value (Y, N, C, MISSING, N/A)")
    AddressMtch: str = Field(..., description="Address match value (Y, N, C, MISSING, N/A)")
    CityMtch: str = Field(..., description="City match value (Y, N, C, MISSING, N/A)")
    StateMtch: str = Field(..., description="State match value (Y, N, C, MISSING, N/A)")
    ZipMtch: str = Field(..., description="Zip match value (Y, N, C, MISSING, N/A)")
    HmPhoneMtch: str = Field(..., description="Home Phone match value (Y, N, C, MISSING, N/A)")
    WkPhoneMtch: str = Field(..., description="Work Phone match value (Y, N, C, MISSING, N/A)")
    IDTypeMtch: str = Field(..., description="ID Type match value (Y, N, C, MISSING, N/A)")
    IDNoMtch: str = Field(..., description="ID Number match value (Y, N, C, MISSING, N/A)")
    IDStateMtch: str = Field(..., description="ID State match value (Y, N, C, MISSING, N/A)")
    OverallMtchScore: float = Field(..., description="Overall match score (0-100)")

class ResultCodeResponse(BaseModel):
    """
    Response model for the get-result-code endpoint.
    """
    customerResultcode: str = Field(..., description="Customer result code (e.g., CRC1000)")

# Configure logging with more detailed format for production
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Configure logging with more detailed format for production
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"{log_dir}/api_{datetime.now().strftime('%Y%m%d')}.log")
    ]
)
logger = logging.getLogger("acc_auth_api")

# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    # Enable docs only in non-production environments
    docs_url=None if ENVIRONMENT == "production" else "/docs",
    redoc_url=None if ENVIRONMENT == "production" else "/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Health check endpoint for production monitoring
@app.get("/health", tags=["system"])
async def health_check():
    """
    Health check endpoint for production monitoring.
    
    Returns:
        Dict with health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": API_VERSION,
        "environment": ENVIRONMENT
    }

@app.post("/get-result-code", tags=["prediction"], response_model=ResultCodeResponse)
async def get_result_code(data: ResultCodeRequest) -> ResultCodeResponse:
    """
    Get the customer result code based on the input data.
    
    This endpoint uses the rule-based model to determine the appropriate
    customer result code based on the input data.
    
    Args:
        data: Input data containing matching fields and scores
        
    Returns:
        Dict with customer result code
    """
    try:
        # Convert Pydantic model to dict
        data_dict = data.model_dump()
        
        # Map the input fields to the expected fields for the rule engine
        mapped_data = {
            "PAINameMtch": data_dict["NameMtch"],
            "SSNMtch": data_dict["SSNMtch"],
            "DOBMtch": data_dict["DOBMtch"],
            "PAIAddressMtch": data_dict["AddressMtch"],
            "HmPhoneMtch": data_dict["HmPhoneMtch"],
            "WkPhoneMtch": data_dict["WkPhoneMtch"],
            "PAIIDMtch": data_dict["IDNoMtch"],
            "OverallMtchScore": data_dict["OverallMtchScore"]
        }
        
        # Use the rule-based model to determine the result code
        result_code = determine_result_code(mapped_data)
        
        # Return the result in the specified format
        return ResultCodeResponse(customerResultcode=result_code)
    except Exception as e:
        # Log the error with more context
        logger.error(f"Error determining result code: {str(e)}", exc_info=True)
        # Raise HTTP exception with appropriate status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={"message": "Error determining result code", "type": "prediction_error"}
        )

if __name__ == "__main__":
    import uvicorn
    
    # Configure uvicorn with appropriate settings
    uvicorn_config = {
        "app": "main:app",
        "host": HOST,
        "port": PORT,
        "log_level": LOG_LEVEL,
        "reload": True,
    }
    
    # Run the server
    uvicorn.run(**uvicorn_config)
