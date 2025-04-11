#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Schemas Module

Contains Pydantic models for API responses.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class PredictionResponse(BaseModel):
    """
    Response model for prediction endpoints.
    
    Attributes:
        customerResultCode (str): The predicted customer result code.
    """
    customerResultCode: str = Field(..., description="The predicted customer result code")


class ClientInfoResponse(BaseModel):
    """
    Response model for client info endpoint.
    
    Attributes:
        client_host (str): The client's host address.
        client_port (int): The client's port number.
    """
    client_host: str = Field(..., description="The client's host address")
    client_port: int = Field(..., description="The client's port number")


class HealthResponse(BaseModel):
    """
    Response model for health check endpoint.
    
    Attributes:
        status (str): The health status of the API.
    """
    status: str = Field(..., description="The health status of the API")


class ErrorResponse(BaseModel):
    """
    Response model for error responses.
    
    Attributes:
        detail (str): The error message.
    """
    detail: str = Field(..., description="The error message") 
