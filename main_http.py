import os
import asyncio
import json
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time

# Import our MCP server components
from mcp_server import (
    MessagingHandler, TemplateHandler, BusinessHandler, MediaHandler,
    FlowHandler, AnalyticsHandler, WebhookHandler, BusinessAccountHandler,
    WhatsAppHandler
)

# Import comprehensive tools
from comprehensive_tools import register_comprehensive_tools
from comprehensive_tools_extended import register_comprehensive_tools_extended

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("whatsapp-mcp-http")

app = FastAPI(
    title="WhatsApp Cloud API MCP Server",
    description="Comprehensive WhatsApp Cloud API integration with 50+ tools including Flows, Analytics, Webhooks, and Business Account Management",
    version="2.0.0"
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
flow_handler = None
analytics_handler = None
webhook_handler = None
business_account_handler = None
whatsapp_handler = None

@app.on_event("startup")
async def startup_event():
    """Initialize handlers on startup"""
    global messaging_handler, template_handler, business_handler, media_handler, whatsapp_handler
    global flow_handler, analytics_handler, webhook_handler, business_account_handler
    
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
        # Initialize core handlers
        messaging_handler = MessagingHandler()
        template_handler = TemplateHandler()
        business_handler = BusinessHandler()
        media_handler = MediaHandler()
        whatsapp_handler = WhatsAppHandler()
        
        # Initialize extended handlers (optional)
        try:
            flow_handler = FlowHandler()
            logger.info("✅ Flow handler initialized")
        except Exception as e:
            logger.warning(f"⚠️ Flow handler not initialized: {e}")
            flow_handler = None
        
        try:
            analytics_handler = AnalyticsHandler()
            logger.info("✅ Analytics handler initialized")
        except Exception as e:
            logger.warning(f"⚠️ Analytics handler not initialized: {e}")
            analytics_handler = None
        
        try:
            webhook_handler = WebhookHandler()
            logger.info("✅ Webhook handler initialized")
        except Exception as e:
            logger.warning(f"⚠️ Webhook handler not initialized: {e}")
            webhook_handler = None
        
        try:
            business_account_handler = BusinessAccountHandler()
            logger.info("✅ Business Account handler initialized")
        except Exception as e:
            logger.warning(f"⚠️ Business Account handler not initialized: {e}")
            business_account_handler = None
        
        logger.info("✅ All handlers initialized successfully")
    except Exception as e:
        logger.error(f"❌ Error initializing handlers: {e}")
        logger.info("🔄 Starting in demo mode")

@app.get("/")
async def root():
    """Root endpoint with server status"""
    status = "demo_mode" if not os.getenv('META_ACCESS_TOKEN') else "active"
    
    return {
        "status": status,
        "message": "WhatsApp Cloud API MCP HTTP Server",
        "version": "2.0.0",
        "description": "Comprehensive WhatsApp Cloud API integration with 50+ tools",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "messaging": "/api/v1/messaging",
            "templates": "/api/v1/templates",
            "business": "/api/v1/business",
            "media": "/api/v1/media",
            "flows": "/api/v1/flows",
            "analytics": "/api/v1/analytics",
            "webhooks": "/api/v1/webhooks",
            "business_account": "/api/v1/business-account"
        },
        "features": [
            "Text, media, interactive messaging",
            "Template management and sending",
            "WhatsApp Flows (interactive experiences)",
            "Analytics and metrics",
            "Webhook management",
            "Business account management",
            "Advanced phone operations"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "WhatsApp Cloud API MCP Server",
        "handlers": {
            "messaging": messaging_handler is not None,
            "templates": template_handler is not None,
            "business": business_handler is not None,
            "media": media_handler is not None,
            "whatsapp": whatsapp_handler is not None,
            "flows": flow_handler is not None,
            "analytics": analytics_handler is not None,
            "webhooks": webhook_handler is not None,
            "business_account": business_account_handler is not None
        },
        "features": {
            "total_tools": "50+ WhatsApp Cloud API tools",
            "messaging": "Text, media, interactive, location, contact",
            "templates": "Create, send, manage message templates",
            "flows": "Interactive WhatsApp experiences",
            "analytics": "Conversation, quality, business metrics",
            "webhooks": "Event subscription management",
            "business": "Account and phone number management"
        }
    }

# ================================
# MESSAGING ENDPOINTS
# ================================

@app.post("/api/v1/messaging/send")
async def send_message(request: Dict[str, Any]):
    """Send a WhatsApp message"""
    if not messaging_handler:
        raise HTTPException(status_code=503, detail="Messaging handler not available")
    
    try:
        phone_number = request.get("phone_number")
        message = request.get("message")
        preview_url = request.get("preview_url", False)
        reply_to_message_id = request.get("reply_to_message_id")
        
        if not phone_number or not message:
            raise HTTPException(status_code=400, detail="phone_number and message are required")
        
        result = await messaging_handler.send_text_message(phone_number, message, preview_url, reply_to_message_id)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return {"status": "error", "error": str(e)}

@app.post("/api/v1/messaging/reaction")
async def send_reaction(request: Dict[str, Any]):
    """Send a reaction to a message"""
    if not messaging_handler:
        raise HTTPException(status_code=503, detail="Messaging handler not available")
    
    try:
        phone_number = request.get("phone_number")
        message_id = request.get("message_id")
        emoji = request.get("emoji", "")
        
        if not phone_number or not message_id:
            raise HTTPException(status_code=400, detail="phone_number and message_id are required")
        
        result = await messaging_handler.send_reaction_message(phone_number, message_id, emoji)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error sending reaction: {e}")
        return {"status": "error", "error": str(e)}

# ================================
# TEMPLATE ENDPOINTS
# ================================

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
        language_code = request.get("language_code", "en_US")
        body_parameters = request.get("body_parameters", [])
        header_parameters = request.get("header_parameters", [])
        reply_to_message_id = request.get("reply_to_message_id")
        
        if not phone_number or not template_name:
            raise HTTPException(status_code=400, detail="phone_number and template_name are required")
        
        result = await template_handler.send_template_message(
            phone_number, template_name, language_code, body_parameters, header_parameters, reply_to_message_id
        )
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error sending template: {e}")
        return {"status": "error", "error": str(e)}

# ================================
# BUSINESS ENDPOINTS
# ================================

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

# ================================
# FLOWS ENDPOINTS
# ================================

@app.get("/api/v1/flows/")
async def list_flows():
    """List all flows"""
    if not flow_handler:
        raise HTTPException(status_code=503, detail="Flow handler not available")
    
    try:
        result = await flow_handler.list_flows()
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error listing flows: {e}")
        return {"status": "error", "error": str(e)}

@app.post("/api/v1/flows/create")
async def create_flow(request: Dict[str, Any]):
    """Create a new flow"""
    if not flow_handler:
        raise HTTPException(status_code=503, detail="Flow handler not available")
    
    try:
        name = request.get("name")
        categories = request.get("categories", [])
        clone_flow_id = request.get("clone_flow_id")
        endpoint_uri = request.get("endpoint_uri")
        
        if not name:
            raise HTTPException(status_code=400, detail="name is required")
        
        result = await flow_handler.create_flow(name, categories, clone_flow_id, endpoint_uri)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error creating flow: {e}")
        return {"status": "error", "error": str(e)}

# ================================
# ANALYTICS ENDPOINTS
# ================================

@app.get("/api/v1/analytics/")
async def get_analytics():
    """Get analytics data"""
    if not analytics_handler:
        raise HTTPException(status_code=503, detail="Analytics handler not available")
    
    try:
        # Get last 7 days analytics
        end_time = int(time.time())
        start_time = end_time - (7 * 24 * 60 * 60)  # 7 days ago
        
        result = await analytics_handler.get_analytics(start_time, end_time, "DAY")
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return {"status": "error", "error": str(e)}

# ================================
# WEBHOOK ENDPOINTS
# ================================

@app.get("/api/v1/webhooks/subscriptions")
async def get_webhook_subscriptions():
    """Get webhook subscriptions"""
    if not webhook_handler:
        raise HTTPException(status_code=503, detail="Webhook handler not available")
    
    try:
        result = await webhook_handler.get_subscriptions()
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error getting webhook subscriptions: {e}")
        return {"status": "error", "error": str(e)}

# ================================
# BUSINESS ACCOUNT ENDPOINTS
# ================================

@app.get("/api/v1/business-account/wabas")
async def get_waba_accounts():
    """Get WABA accounts"""
    if not business_account_handler:
        raise HTTPException(status_code=503, detail="Business Account handler not available")
    
    try:
        result = await business_account_handler.get_owned_wabas()
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error getting WABA accounts: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
