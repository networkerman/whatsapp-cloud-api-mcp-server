#!/usr/bin/env python3
"""
WhatsApp Cloud API SSE Server - Simplified for ElevenLabs
FastAPI-based SSE server that's compatible with MCP clients
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
from dotenv import load_dotenv

# Import your MCP handlers
from mcp_server import (
    MessagingHandler, TemplateHandler, BusinessHandler, MediaHandler
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("whatsapp-sse-simple")

# Create FastAPI app
app = FastAPI(
    title="WhatsApp Cloud API SSE Server",
    description="SSE server for WhatsApp Cloud API MCP integration",
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

@app.on_event("startup")
async def startup_event():
    """Initialize handlers on startup."""
    global messaging_handler, template_handler, business_handler, media_handler
    
    # Check for environment variables
    required_vars = ["META_ACCESS_TOKEN", "META_PHONE_NUMBER_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"⚠️  Missing required environment variables: {missing_vars}")
        logger.info("🔧 SSE server will run in demo mode")
        return
    
    # Optional but recommended for full functionality
    optional_vars = ["META_BUSINESS_ACCOUNT_ID", "WABA_ID"]
    missing_optional = [var for var in optional_vars if not os.getenv(var)]
    if missing_optional:
        logger.info(f"ℹ️  Optional environment variables not set: {missing_optional}")
    
    try:
        messaging_handler = MessagingHandler()
        template_handler = TemplateHandler()
        business_handler = BusinessHandler()
        media_handler = MediaHandler()
        logger.info("✅ All handlers initialized successfully")
        logger.info("🚀 WhatsApp Cloud API functionality is active")
    except Exception as e:
        logger.warning(f"⚠️  Handler initialization failed: {e}")
        logger.info("🔧 SSE server running in demo mode")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "WhatsApp Cloud API SSE Server",
        "handlers_initialized": all([
            messaging_handler, template_handler, business_handler, media_handler
        ])
    }

# Root endpoint
@app.get("/")
async def root():
    """API information."""
    handlers_active = all([messaging_handler, template_handler, business_handler, media_handler])
    
    return {
        "service": "WhatsApp Cloud API SSE Server",
        "version": "1.0.0",
        "author": "Udayan Das Chowdhury",
        "status": "active" if handlers_active else "demo_mode",
        "whatsapp_functionality": "enabled" if handlers_active else "disabled - configure environment variables",
        "sse_endpoint": "/sse",
        "health": "/health",
        "github": "https://github.com/networkerman/whatsapp-cloud-api-mcp-server",
        "mcp_tools": {
            "send_text_message": "Send WhatsApp text messages",
            "send_template_message": "Send WhatsApp template messages",
            "get_templates": "List available templates",
            "get_business_profile": "Get business profile information"
        }
    }

# MCP Tool implementations
async def execute_mcp_tool(tool_name: str, arguments: dict) -> dict:
    """Execute MCP tool and return result."""
    try:
        if tool_name == "send_text_message":
            if not messaging_handler:
                return {"status": "error", "message": "Messaging handler not initialized"}
            
            result = await messaging_handler.send_text_message(
                arguments.get("phone_number"),
                arguments.get("message"),
                arguments.get("preview_url", False)
            )
            return result
            
        elif tool_name == "send_template_message":
            if not template_handler:
                return {"status": "error", "message": "Template handler not initialized"}
            
            result = await template_handler.send_template_message(
                arguments.get("phone_number"),
                arguments.get("template_name"),
                arguments.get("language_code", "en_US"),
                arguments.get("body_parameters", [])
            )
            return result
            
        elif tool_name == "get_templates":
            if not template_handler:
                return {"status": "error", "message": "Template handler not initialized"}
            
            result = await template_handler.get_message_templates()
            return result
            
        elif tool_name == "get_business_profile":
            if not business_handler:
                return {"status": "error", "message": "Business handler not initialized"}
            
            result = await business_handler.get_business_profile()
            return result
            
        else:
            return {"status": "error", "message": f"Unknown tool: {tool_name}"}
            
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return {"status": "error", "message": str(e)}

# SSE endpoint for MCP communication
@app.get("/sse")
async def sse_endpoint(request: Request):
    """SSE endpoint for MCP client communication."""
    
    async def event_stream():
        try:
            # Send initial connection message
            yield f"data: {json.dumps({'type': 'connected', 'message': 'WhatsApp MCP SSE Server connected'})}\n\n"
            
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
                },
                {
                    "name": "get_templates",
                    "description": "Get available WhatsApp templates",
                    "parameters": {}
                },
                {
                    "name": "get_business_profile",
                    "description": "Get WhatsApp business profile",
                    "parameters": {}
                }
            ]
            
            yield f"data: {json.dumps({'type': 'tools', 'tools': tools})}\n\n"
            
            # Keep connection alive
            while True:
                if await request.is_disconnected():
                    break
                
                # Send heartbeat every 30 seconds
                yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': asyncio.get_event_loop().time()})}\n\n"
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

# POST endpoint for MCP tool calls
@app.post("/mcp/call")
async def mcp_call(request: dict):
    """Handle MCP tool calls via POST."""
    tool_name = request.get("tool")
    arguments = request.get("arguments", {})
    
    if not tool_name:
        return {"status": "error", "message": "Missing tool name"}
    
    result = await execute_mcp_tool(tool_name, arguments)
    return result

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    
    logger.info(f"🚀 Starting WhatsApp SSE Server (Simplified)")
    logger.info(f"🌐 Server will be available at: http://{host}:{port}")
    logger.info(f"📡 SSE endpoint: http://{host}:{port}/sse")
    logger.info(f"🔍 Health check: http://{host}:{port}/health")
    logger.info(f"🛠️  MCP calls: http://{host}:{port}/mcp/call")
    
    uvicorn.run(
        "server_sse_simple:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )