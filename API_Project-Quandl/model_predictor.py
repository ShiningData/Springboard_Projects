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
from create_pai_mapping import create_pai_features
from validate_data import validate_matches
from models import AccAuthModel, MatchStatus

# Define response model for the API
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
async def get_result_code(data: AccAuthModel) -> ResultCodeResponse:
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
        # Use the model's built-in validation
        validation_result = data.validate_business_rules()
        if not validation_result.valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": validation_result.error,
                    "type": validation_result.error_type.name if validation_result.error_type else "validation_error",
                    "field": validation_result.field_name
                }
            )
        
        # Convert model to dict for further processing
        data_dict = data.model_dump()
        
        # Use the create_pai_features function to map the input fields to PAI features
        mapped_data = create_pai_features(data_dict)
        
        # Use the rule-based model to determine the result code
        result_code = determine_result_code(mapped_data)
        
        # Return the result in the specified format
        return ResultCodeResponse(customerResultcode=result_code)
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
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
