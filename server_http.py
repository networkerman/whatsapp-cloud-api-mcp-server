import os
import asyncio
import json
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import our MCP server components
from mcp_server import (
    MessagingHandler,
    TemplateHandler,
    BusinessHandler,
    MediaHandler,
    WhatsAppHandler
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("whatsapp-mcp-http")

app = FastAPI(
    title="WhatsApp Cloud API MCP Server",
    description="HTTP REST API server for WhatsApp Cloud API MCP integration",
    version="1.0.0"
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
whatsapp_handler = None

@app.on_event("startup")
async def startup_event():
    """Initialize handlers on startup"""
    global messaging_handler, template_handler, business_handler, media_handler, whatsapp_handler
    
    logger.info("🚀 Starting WhatsApp MCP HTTP Server")
    logger.info(f"🌐 Server will be available at: http://0.0.0.0:{os.getenv('PORT', '8080')}")
    logger.info(f"📚 API Documentation: http://0.0.0.0:{os.getenv('PORT', '8080')}/docs")
    logger.info(f"🔧 Health Check: http://0.0.0.0:{os.getenv('PORT', '8080')}/health")
    
    # Check required environment variables
    required_vars = ['META_ACCESS_TOKEN', 'META_PHONE_NUMBER_ID']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"⚠️ Missing required environment variables: {missing_vars}")
        logger.warning("🔄 Starting in demo mode - some features may be limited")
        logger.info("💡 Set META_ACCESS_TOKEN and META_PHONE_NUMBER_ID for full functionality")
    else:
        logger.info("✅ All required environment variables found")
    
    try:
        # Initialize handlers
        messaging_handler = MessagingHandler()
        template_handler = TemplateHandler()
        business_handler = BusinessHandler()
        media_handler = MediaHandler()
        whatsapp_handler = WhatsAppHandler()
        
        logger.info("✅ All handlers initialized successfully")
    except Exception as e:
        logger.error(f"❌ Error initializing handlers: {e}")
        logger.info("🔄 Starting in demo mode")

@app.get("/")
async def root():
    """Root endpoint with server status"""
    status = "demo_mode" if not os.getenv('META_ACCESS_TOKEN') else "active"
    whatsapp_status = "available" if business_handler else "unavailable"
    
    return {
        "status": status,
        "message": "WhatsApp Cloud API MCP HTTP Server",
        "whatsapp_functionality": whatsapp_status,
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "sse": "/sse",
            "messaging": "/api/v1/messaging",
            "templates": "/api/v1/templates",
            "business": "/api/v1/business",
            "media": "/api/v1/media"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": asyncio.get_event_loop().time(),
        "handlers": {
            "messaging": messaging_handler is not None,
            "templates": template_handler is not None,
            "business": business_handler is not None,
            "media": media_handler is not None,
            "whatsapp": whatsapp_handler is not None
        }
    }

@app.get("/sse")
async def sse_endpoint():
    """Server-Sent Events endpoint for MCP client communication"""
    async def event_stream():
        # Send initial connection message
        yield f"data: {json.dumps({'type': 'connection', 'message': 'Connected to WhatsApp MCP Server'})}\n\n"
        
        # Send available tools
        tools = [
            {
                "name": "send_whatsapp_message",
                "description": "Send a WhatsApp message to a phone number",
                "parameters": {
                    "phone_number": "string",
                    "message": "string"
                }
            },
            {
                "name": "send_template_message",
                "description": "Send a WhatsApp template message",
                "parameters": {
                    "phone_number": "string",
                    "template_name": "string",
                    "parameters": "object"
                }
            },
            {
                "name": "get_business_profile",
                "description": "Get WhatsApp business profile information",
                "parameters": {}
            },
            {
                "name": "get_message_templates",
                "description": "Get available message templates",
                "parameters": {}
            }
        ]
        
        yield f"data: {json.dumps({'type': 'tools', 'tools': tools})}\n\n"
        
        # Send heartbeat every 30 seconds
        while True:
            await asyncio.sleep(30)
            yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': asyncio.get_event_loop().time()})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )

# API Routes
@app.post("/api/v1/messaging/send")
async def send_message(request: Dict[str, Any]):
    """Send a WhatsApp message"""
    if not messaging_handler:
        raise HTTPException(status_code=503, detail="Messaging handler not available")
    
    try:
        phone_number = request.get("phone_number")
        message = request.get("message")
        
        if not phone_number or not message:
            raise HTTPException(status_code=400, detail="phone_number and message are required")
        
        result = await messaging_handler.send_text_message(phone_number, message)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return {"status": "error", "error": str(e)}

@app.get("/api/v1/templates/")
async def get_templates():
    """Get all message templates"""
    if not template_handler:
        raise HTTPException(status_code=503, detail="Template handler not available")
    
    try:
        result = await template_handler.get_message_templates()
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error getting templates: {e}")
        return {"status": "error", "error": str(e)}

@app.post("/api/v1/templates/send")
async def send_template(request: Dict[str, Any]):
    """Send a template message"""
    if not template_handler:
        raise HTTPException(status_code=503, detail="Template handler not available")
    
    try:
        phone_number = request.get("phone_number")
        template_name = request.get("template_name")
        parameters = request.get("parameters", {})
        
        if not phone_number or not template_name:
            raise HTTPException(status_code=400, detail="phone_number and template_name are required")
        
        result = await template_handler.send_template_message(phone_number, template_name, parameters)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error sending template: {e}")
        return {"status": "error", "error": str(e)}

@app.get("/api/v1/business/profile")
async def get_business_profile():
    """Get business profile"""
    if not business_handler:
        raise HTTPException(status_code=503, detail="Business handler not available")
    
    try:
        result = await business_handler.get_business_profile()
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error getting business profile: {e}")
        return {"status": "error", "error": str(e)}

@app.get("/api/v1/business/phone-numbers")
async def get_phone_numbers():
    """Get business phone numbers"""
    if not business_handler:
        raise HTTPException(status_code=503, detail="Business handler not available")
    
    try:
        result = await business_handler.get_phone_numbers()
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error getting phone numbers: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port) 