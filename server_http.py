#!/usr/bin/env python3
"""
WhatsApp Cloud API MCP Server - HTTP REST API
Deploys the MCP server as a traditional HTTP REST API for maximum compatibility.
"""

import os
import logging
import asyncio
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn

# Import your MCP handlers
from mcp_server import (
    MessagingHandler, TemplateHandler, BusinessHandler, MediaHandler,
    WhatsAppHandler
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("whatsapp-mcp-http")

# Pydantic models for API requests
class TextMessageRequest(BaseModel):
    phone_number: str = Field(..., description="Recipient phone number with country code")
    message: str = Field(..., description="Message text to send")
    preview_url: bool = Field(False, description="Enable URL preview")

class TemplateMessageRequest(BaseModel):
    phone_number: str = Field(..., description="Recipient phone number with country code")
    template_name: str = Field(..., description="Name of the template to send")
    language_code: str = Field(..., description="Language code (e.g., en_US)")
    body_parameters: List[str] = Field(default=[], description="Template body parameters")
    header_parameters: List[str] = Field(default=[], description="Template header parameters")

class MediaMessageRequest(BaseModel):
    phone_number: str = Field(..., description="Recipient phone number with country code")
    media_id: Optional[str] = Field(None, description="Media ID from upload")
    media_url: Optional[str] = Field(None, description="Media URL")
    caption: Optional[str] = Field(None, description="Media caption")
    filename: Optional[str] = Field(None, description="Filename for documents")

class ButtonMessageRequest(BaseModel):
    phone_number: str = Field(..., description="Recipient phone number with country code")
    body_text: str = Field(..., description="Message body text")
    buttons: List[Dict[str, str]] = Field(..., description="List of buttons with title and id")
    header_text: Optional[str] = Field(None, description="Optional header text")
    footer_text: Optional[str] = Field(None, description="Optional footer text")

# Initialize FastAPI app
app = FastAPI(
    title="WhatsApp Cloud API MCP Server",
    description="HTTP REST API for WhatsApp Cloud API operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global handlers
messaging_handler = None
template_handler = None
business_handler = None
media_handler = None

@app.on_event("startup")
async def startup_event():
    """Initialize handlers on startup."""
    global messaging_handler, template_handler, business_handler, media_handler
    
    # Check for environment variables
    required_vars = ["META_ACCESS_TOKEN", "META_PHONE_NUMBER_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"⚠️  Missing environment variables: {missing_vars}")
        logger.info("🔧 Server will run in demo mode - configure environment variables to enable WhatsApp functionality")
        logger.info("📚 See deployment documentation: https://github.com/networkerman/whatsapp-cloud-api-mcp-server#deployment")
        return
    
    # Optional but recommended for full functionality
    optional_vars = ["META_BUSINESS_ACCOUNT_ID", "WABA_ID"]
    missing_optional = [var for var in optional_vars if not os.getenv(var)]
    if missing_optional:
        logger.info(f"ℹ️  Optional environment variables not set: {missing_optional}")
        logger.info("💡 Set both META_BUSINESS_ACCOUNT_ID and WABA_ID for maximum API compatibility")
    
    try:
        messaging_handler = MessagingHandler()
        template_handler = TemplateHandler()
        business_handler = BusinessHandler()
        media_handler = MediaHandler()
        logger.info("✅ All handlers initialized successfully")
        logger.info("🚀 WhatsApp Cloud API functionality is active")
    except Exception as e:
        logger.warning(f"⚠️  Handler initialization failed: {e}")
        logger.info("🔧 Server running in demo mode - check your WhatsApp API credentials")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "WhatsApp Cloud API MCP Server",
        "handlers_initialized": all([
            messaging_handler, template_handler, business_handler, media_handler
        ])
    }

# API Information
@app.get("/")
async def root():
    """API information."""
    handlers_active = all([messaging_handler, template_handler, business_handler, media_handler])
    
    return {
        "service": "WhatsApp Cloud API MCP Server",
        "version": "1.0.0",
        "author": "Udayan Das Chowdhury",
        "status": "active" if handlers_active else "demo_mode",
        "whatsapp_functionality": "enabled" if handlers_active else "disabled - configure environment variables",
        "documentation": "/docs",
        "health": "/health",
        "github": "https://github.com/networkerman/whatsapp-cloud-api-mcp-server",
        "endpoints": {
            "messaging": "/api/v1/messaging/",
            "templates": "/api/v1/templates/",
            "business": "/api/v1/business/",
            "media": "/api/v1/media/"
        },
        "setup_guide": "https://github.com/networkerman/whatsapp-cloud-api-mcp-server#deployment" if not handlers_active else None
    }

# ================================
# MESSAGING ENDPOINTS
# ================================

@app.post("/api/v1/messaging/send-text")
async def send_text_message(request: TextMessageRequest):
    """Send a text message via WhatsApp."""
    if not messaging_handler:
        raise HTTPException(status_code=503, detail="Messaging handler not initialized")
    
    try:
        result = await messaging_handler.send_text_message(
            request.phone_number,
            request.message,
            request.preview_url
        )
        return result
    except Exception as e:
        logger.error(f"Error sending text message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/messaging/send-image")
async def send_image_message(request: MediaMessageRequest):
    """Send an image message via WhatsApp."""
    if not messaging_handler:
        raise HTTPException(status_code=503, detail="Messaging handler not initialized")
    
    try:
        result = await messaging_handler.send_image_message(
            request.phone_number,
            request.media_id,
            request.media_url,
            request.caption
        )
        return result
    except Exception as e:
        logger.error(f"Error sending image message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/messaging/send-button")
async def send_button_message(request: ButtonMessageRequest):
    """Send a button message via WhatsApp."""
    if not messaging_handler:
        raise HTTPException(status_code=503, detail="Messaging handler not initialized")
    
    try:
        result = await messaging_handler.send_button_message(
            request.phone_number,
            request.body_text,
            request.buttons,
            request.header_text,
            request.footer_text
        )
        return result
    except Exception as e:
        logger.error(f"Error sending button message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================
# TEMPLATE ENDPOINTS
# ================================

@app.get("/api/v1/templates/")
async def get_templates():
    """Get all message templates."""
    if not template_handler:
        raise HTTPException(status_code=503, detail="Template handler not initialized")
    
    try:
        result = await template_handler.get_message_templates()
        return result
    except Exception as e:
        logger.error(f"Error getting templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/templates/send")
async def send_template_message(request: TemplateMessageRequest):
    """Send a template message via WhatsApp."""
    if not template_handler:
        raise HTTPException(status_code=503, detail="Template handler not initialized")
    
    try:
        result = await template_handler.send_template_message(
            request.phone_number,
            request.template_name,
            request.language_code,
            request.body_parameters,
            request.header_parameters
        )
        return result
    except Exception as e:
        logger.error(f"Error sending template message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================
# BUSINESS ENDPOINTS
# ================================

@app.get("/api/v1/business/profile")
async def get_business_profile():
    """Get business profile information."""
    if not business_handler:
        raise HTTPException(status_code=503, detail="Business handler not initialized")
    
    try:
        result = await business_handler.get_business_profile()
        return result
    except Exception as e:
        logger.error(f"Error getting business profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/business/phone-numbers")
async def get_phone_numbers():
    """Get all business phone numbers."""
    if not business_handler:
        raise HTTPException(status_code=503, detail="Business handler not initialized")
    
    try:
        result = await business_handler.get_phone_numbers()
        return result
    except Exception as e:
        logger.error(f"Error getting phone numbers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================
# MEDIA ENDPOINTS  
# ================================

@app.get("/api/v1/media/{media_id}")
async def get_media_info(media_id: str):
    """Get information about uploaded media."""
    if not media_handler:
        raise HTTPException(status_code=503, detail="Media handler not initialized")
    
    try:
        result = await media_handler.get_media_info(media_id)
        return result
    except Exception as e:
        logger.error(f"Error getting media info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================
# RESOURCES ENDPOINTS
# ================================

@app.get("/api/v1/resources/contacts")
async def get_contacts():
    """Get sample contacts."""
    contacts = [
        {"name": "João da Silva", "phone_number": "+55629999999999"},
        {"name": "Test Contact", "phone_number": "+1234567890"},
    ]
    return {"status": "success", "data": contacts}

# ================================
# SSE ENDPOINT FOR MCP CLIENTS
# ================================

@app.get("/sse")
async def sse_endpoint(request: Request):
    """SSE endpoint for MCP client communication (ElevenLabs, etc.)."""
    
    async def event_stream():
        try:
            import json
            
            # Send initial connection message
            yield f"data: {json.dumps({'type': 'connected', 'service': 'WhatsApp Cloud API MCP Server'})}\n\n"
            
            # Send available tools
            tools = [
                {
                    "name": "send_text_message",
                    "description": "Send a WhatsApp text message",
                    "parameters": {
                        "phone_number": "string",
                        "message": "string", 
                        "preview_url": "boolean"
                    }
                },
                {
                    "name": "send_template_message", 
                    "description": "Send a WhatsApp template message",
                    "parameters": {
                        "phone_number": "string",
                        "template_name": "string",
                        "language_code": "string",
                        "body_parameters": "array"
                    }
                }
            ]
            
            yield f"data: {json.dumps({'type': 'tools', 'tools': tools})}\n\n"
            
            # Keep connection alive
            while True:
                if await request.is_disconnected():
                    break
                
                # Send heartbeat every 30 seconds
                yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': 'alive'})}\n\n"
                await asyncio.sleep(30)
                
        except Exception as e:
            logger.error(f"SSE stream error: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

if __name__ == "__main__":
    host = os.getenv("HTTP_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("HTTP_SERVER_PORT", "8080"))
    
    logger.info(f"🚀 Starting WhatsApp MCP HTTP Server")
    logger.info(f"🌐 Server will be available at: http://{host}:{port}")
    logger.info(f"📚 API Documentation: http://{host}:{port}/docs")
    logger.info(f"🔧 Health Check: http://{host}:{port}/health")
    
    uvicorn.run(
        "server_http:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )