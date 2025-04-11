#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Error Handlers Module

Contains custom exception handlers for the FastAPI application.
"""
from fastapi import Request
from fastapi.responses import JSONResponse
import logging

from schemas import ErrorResponse

# Configure logging
logger = logging.getLogger("acc_auth_api")


async def value_error_handler(request: Request, exc: ValueError):
    """
    Handler for ValueError exceptions.
    
    Args:
        request: The request that caused the error
        exc: The ValueError exception
        
    Returns:
        JSONResponse: A 400 Bad Request response with the error details
    """
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(detail=str(exc)).model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handler for general exceptions.
    
    Args:
        request: The request that caused the error
        exc: The exception
        
    Returns:
        JSONResponse: A 500 Internal Server Error response
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(detail="Internal server error").model_dump()
    ) 
