#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prediction Routes Module

Contains API routes for prediction endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import logging

from models import acc_auth_model
from schemas import PredictionResponse, ErrorResponse
from services.prediction_service import acc_auth_prediction, validate_request

# Configure logging
logger = logging.getLogger("acc_auth_api")

# Create router
router = APIRouter(
    prefix="/prediction",
    tags=["prediction"],
    responses={
        404: {"model": ErrorResponse, "description": "Not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
)


@router.post("/acc_auth/", 
          status_code=status.HTTP_200_OK, 
          response_model=PredictionResponse,
          response_model_exclude_none=True)
async def predict_api(request_data: Dict[str, Any] = Depends(validate_request)):
    """
    Predict the result code for bank account authentication based on
    the provided input data.
    
    Parameters:
        request_data: Validated dictionary data from the request
        
    Returns:
        PredictionResponse: A dictionary containing the predicted authentication result.
    """
    try:
        return acc_auth_prediction(request_data)
    except ValueError as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") 

===================================================================================================

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
System Router Module

Contains system-related endpoints like health checks and client information.
"""
from fastapi import APIRouter
from typing import Dict

# Create router
router = APIRouter(
    prefix="/system",
    tags=["system"]
)

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Dict[str, str]: Status message indicating the API is healthy
    """
    return {"status": "healthy"}

@router.get("/client_info")
async def client_info() -> Dict[str, str]:
    """
    Client information endpoint.
    
    Returns:
        Dict[str, str]: Client information including version and environment
    """
    return {
        "version": "0.0.1",
        "environment": "development",
        "status": "active"
    } 

===========================================================

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
System Routes Module

Contains API routes for system-related endpoints like health checks.
"""
from fastapi import APIRouter, Request
import logging

from schemas import ClientInfoResponse, HealthResponse, ErrorResponse

# Configure logging
logger = logging.getLogger("acc_auth_api")

# Create router
router = APIRouter(
    prefix="",
    tags=["system"],
    responses={
        404: {"model": ErrorResponse, "description": "Not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
)


@router.get("/client/", response_model=ClientInfoResponse)
def client_info(request: Request):
    """
    Retrieve and return the client's host and port information.
    
    Parameters:
        request (Request): The incoming HTTP request object containing
        client details.
        
    Returns:
        ClientInfoResponse: A dictionary with the client's host and port information
    """
    return {
        "client_host": request.client.host,
        "client_port": request.client.port,
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Simple health check endpoint
    
    Returns:
        HealthResponse: A dictionary with the health status
    """
    return {"status": "healthy"} 

