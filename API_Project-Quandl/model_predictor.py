#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Routers Package

Contains all API route modules for the rule engine application.
Routes are organized by domain (prediction, system) for better maintainability.
"""
from routers.prediction_routes import router as prediction_router
from routers.system_routes import router as system_router

__all__ = ["prediction_router", "system_router"] 

===========================================

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prediction Routes Module

Contains API routes for prediction endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Dict, Any
import logging
from datetime import datetime

from models import AccAuthModel
from services.prediction_service import acc_auth_prediction, validate_request, clear_caches

# Configure logging
logger = logging.getLogger("acc_auth_api")

# Create router
router = APIRouter(
    prefix="",
    tags=["prediction"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    },
)

@router.post("/get-result-code", 
          status_code=status.HTTP_200_OK,
          response_model=Dict[str, str])
async def get_result_code(data: AccAuthModel, request: Request):
    """
    Get the customer result code based on the input data.
    
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
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error determining result code: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={"message": "Error determining result code", "type": "prediction_error"}
        )

@router.post("/clear-caches")
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
        logger.error(f"Error clearing caches: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={"message": "Error clearing caches", "type": "system_error"}
        ) 


==============================

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

===============================

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
System Routes Module

Contains API routes for system-related endpoints like health checks.
"""
from fastapi import APIRouter, Request, HTTPException, status
from typing import Dict, Any
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger("acc_auth_api")

# Create router
router = APIRouter(
    prefix="",
    tags=["system"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)

@router.post("/get-client-info")
async def get_client_info(request: Request) -> Dict[str, Any]:
    """
    Get client information based on the request.
    
    Args:
        request: FastAPI request object for client information
        
    Returns:
        Dict with client information
    """
    try:
        # Get client information from the request
        client_host = request.client.host
        client_port = request.client.port
        
        # Create client info object
        client_info = {
            "clientId": f"{client_host}:{client_port}",
            "clientHost": client_host,
            "clientPort": client_port,
            "lastUpdated": datetime.now().isoformat()
        }
        
        return {"client": client_info}
    except Exception as e:
        logger.error(f"Error retrieving client info: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={"message": "Error retrieving client information", "type": "database_error"}
        )

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for production monitoring.
    
    Returns:
        Dict with health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    } 

