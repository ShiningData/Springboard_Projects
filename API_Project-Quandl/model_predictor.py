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

from fastapi import FastAPI, HTTPException, status, Depends, Request
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
from models import AccAuthModel
from services.prediction_service import (
    acc_auth_prediction, 
    validate_request,
    clear_caches
)

# Define response model for the API
class ResultCodeResponse(BaseModel):
    """
    Response model for the get-result-code endpoint.
    """
    customerResultcode: str = Field(..., description="Customer result code (e.g., CRC1000)")

# Define models for client info endpoint
class ClientInfoRequest(BaseModel):
    """
    Request model for the get-client-info endpoint.
    """
    clientId: str = Field(..., description="Unique identifier for the client")

class ClientInfo(BaseModel):
    """
    Model for client information.
    """
    clientId: str = Field(..., description="Unique identifier for the client")
    clientHost: str = Field(..., description="Client's host address")
    clientPort: int = Field(..., description="Client's port number")
    lastUpdated: datetime = Field(default_factory=datetime.now, description="Last time client info was updated")

class ClientInfoResponse(BaseModel):
    """
    Response model for the get-client-info endpoint.
    """
    client: ClientInfo = Field(..., description="Client information")

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
async def get_result_code(data: AccAuthModel, request: Request) -> ResultCodeResponse:
    """
    Get the customer result code based on the input data.
    
    This endpoint uses the rule-based model to determine the appropriate
    customer result code based on the input data.
    
    Args:
        data: Input data containing matching fields and scores
        request: FastAPI request object for client information
        
    Returns:
        Dict with customer result code
    """
    try:
        # Log client information
        client_host = request.client.host
        client_port = request.client.port
        logger.info(f"Request from client: {client_host}:{client_port}")
        
        # Convert model to dict for processing
        data_dict = data.model_dump()
        
        # Use the prediction service to get the result code
        result = acc_auth_prediction(data_dict)
        
        # Return the result in the specified format
        return ResultCodeResponse(customerResultcode=result["customerResultCode"])
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

@app.post("/get-client-info", tags=["client"], response_model=ClientInfoResponse)
async def get_client_info(data: ClientInfoRequest, request: Request) -> ClientInfoResponse:
    """
    Get client information based on the client ID.
    
    This endpoint retrieves client information including host and port.
    
    Args:
        data: Input data containing client ID
        request: FastAPI request object for client information
        
    Returns:
        Client information including host and port
    """
    try:
        # Get client information from the request
        client_host = request.client.host
        client_port = request.client.port
        
        # Create client info object
        client = ClientInfo(
            clientId=data.clientId,
            clientHost=client_host,
            clientPort=client_port,
            lastUpdated=datetime.now()
        )
        
        # Return the client info
        return ClientInfoResponse(client=client)
    except Exception as e:
        # Log the error with more context
        logger.error(f"Error retrieving client info: {str(e)}", exc_info=True)
        # Raise HTTP exception with appropriate status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={"message": "Error retrieving client information", "type": "database_error"}
        )

@app.post("/clear-caches", tags=["system"])
async def clear_caches_endpoint():
    """
    Clear all caches used by the prediction service.
    
    Returns:
        Dict with status
    """
    try:
        clear_caches()
        return {"status": "success", "message": "All caches cleared"}
    except Exception as e:
        # Log the error with more context
        logger.error(f"Error clearing caches: {str(e)}", exc_info=True)
        # Raise HTTP exception with appropriate status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={"message": "Error clearing caches", "type": "system_error"}
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
