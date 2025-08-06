from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

# Import all handlers
from mcp_server import (
    MessagingHandler, TemplateHandler, BusinessHandler, MediaHandler,
    FlowHandler, AnalyticsHandler, WebhookHandler, BusinessAccountHandler,
    WhatsAppHandler, WhatsAppMessage  # Legacy support
)

# Load environment variables
load_dotenv()

# Initialize all handlers
messaging_handler = None
template_handler = None
business_handler = None
media_handler = None
flow_handler = None
analytics_handler = None
webhook_handler = None
business_account_handler = None
legacy_handler = None

# Check for required environment variables first
required_vars = ["META_ACCESS_TOKEN", "META_PHONE_NUMBER_ID"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print("❌ ERROR: Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\n📝 Please create a .env file with the required variables.")
    print("   You can copy env_template.txt to .env and fill in your values.")
    print("   Get your credentials from: https://developers.facebook.com/")
    print("\n🔧 For testing, you can also set these as environment variables:")
    for var in missing_vars:
        print(f"   export {var}=your_value_here")
    
    # Exit gracefully instead of continuing with None handlers
    import sys
    sys.exit(1)

try:
    messaging_handler = MessagingHandler()
    template_handler = TemplateHandler()
    business_handler = BusinessHandler()
    media_handler = MediaHandler()
    
    # Initialize new handlers (optional - they may not have all required env vars)
    try:
        flow_handler = FlowHandler()
        print("✅ Flow handler initialized")
    except Exception as e:
        print(f"⚠️  Flow handler not initialized: {e}")
        flow_handler = None
    
    try:
        analytics_handler = AnalyticsHandler()
        print("✅ Analytics handler initialized")
    except Exception as e:
        print(f"⚠️  Analytics handler not initialized: {e}")
        analytics_handler = None
    
    try:
        webhook_handler = WebhookHandler()
        print("✅ Webhook handler initialized")
    except Exception as e:
        print(f"⚠️  Webhook handler not initialized: {e}")
        webhook_handler = None
    
    try:
        business_account_handler = BusinessAccountHandler()
        print("✅ Business Account handler initialized")
    except Exception as e:
        print(f"⚠️  Business Account handler not initialized: {e}")
        business_account_handler = None
    
    # Legacy handler for backward compatibility
    legacy_handler = WhatsAppHandler()
    print("✅ All core handlers initialized successfully")
except Exception as e:
    print(f"❌ ERROR: Failed to initialize core handlers: {e}")
    print("Please check your environment variables and try again.")
    import sys
    sys.exit(1)

# Create FastMCP app
mcp = FastMCP()

# Sample contacts for the resource
contacts = [
    {"name": "João da Silva", "phone_number": "+55629999999999"},
    {"name": "Test Contact", "phone_number": "+1234567890"},
]

# ================================
# LEGACY TOOLS (Backward Compatibility)
# ================================

@mcp.tool()
async def send_whatsapp_message(phone_number: str, message: str) -> dict:
    """
    Send a basic WhatsApp text message (legacy function for backward compatibility).
    
    Args:
        phone_number: The recipient's phone number (with country code, e.g., +5511999999999)
        message: The message to send
        
    Returns:
        dict: Response containing status and message details
    """
    if messaging_handler is None:
        return {"status": "error", "message": "Handler not initialized. Please check environment variables."}
    
    try:
        return await messaging_handler.send_text_message(phone_number, message)
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ================================
# REGISTER COMPREHENSIVE TOOLS
# ================================

# Import and register all comprehensive tools
try:
    from comprehensive_tools import register_comprehensive_tools
    register_comprehensive_tools(mcp, messaging_handler, template_handler, business_handler, media_handler)
    print("✅ Core comprehensive tools registered successfully")
except Exception as e:
    print(f"❌ ERROR: Could not register core comprehensive tools: {e}")
    import sys
    sys.exit(1)

# Import and register extended comprehensive tools (new features)
try:
    from comprehensive_tools_extended import register_comprehensive_tools_extended
    register_comprehensive_tools_extended(
        mcp, messaging_handler, template_handler, business_handler, media_handler,
        flow_handler, analytics_handler, webhook_handler, business_account_handler
    )
    print("✅ Extended comprehensive tools registered successfully")
except Exception as e:
    print(f"⚠️  Could not register extended comprehensive tools: {e}")
    print("Some advanced features may not be available")

# ================================
# RESOURCES
# ================================

@mcp.resource("resource://contacts")
async def get_contacts() -> List[Dict[str, str]]:
    """
    Get a list of contacts with their names and phone numbers.
    
    Returns:
        List[Dict[str, str]]: A list of contacts with name and phone_number
    """
    return contacts

@mcp.resource("resource://templates")
async def get_templates_resource() -> dict:
    """
    Get message templates as a resource.
    
    Returns:
        dict: Templates data
    """
    if template_handler is None:
        return {"status": "error", "message": "Template handler not initialized", "data": []}
    
    try:
        return await template_handler.get_message_templates()
    except Exception as e:
        return {"status": "error", "message": str(e), "data": []}

@mcp.resource("resource://business_profile")
async def get_business_profile_resource() -> dict:
    """
    Get business profile as a resource.
    
    Returns:
        dict: Business profile data
    """
    if business_handler is None:
        return {"status": "error", "message": "Business handler not initialized", "data": {}}
    
    try:
        return await business_handler.get_business_profile()
    except Exception as e:
        return {"status": "error", "message": str(e), "data": {}}

@mcp.resource("resource://flows")
async def get_flows_resource() -> dict:
    """Get flows as a resource"""
    if flow_handler is None:
        return {"status": "error", "message": "Flow handler not initialized", "data": []}
    
    try:
        result = await flow_handler.list_flows()
        return {
            "status": "success",
            "data": result,
            "description": "WhatsApp Flows Information"
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "data": []}

@mcp.resource("resource://analytics_summary")
async def get_analytics_summary_resource() -> dict:
    """Get analytics summary as a resource"""
    if analytics_handler is None:
        return {"status": "error", "message": "Analytics handler not initialized", "data": {}}
    
    try:
        # Get last 7 days analytics
        import time
        end_time = int(time.time())
        start_time = end_time - (7 * 24 * 60 * 60)  # 7 days ago
        
        result = await analytics_handler.get_analytics(start_time, end_time, "DAY")
        return {
            "status": "success",
            "data": result,
            "description": "WhatsApp Analytics Summary (Last 7 Days)"
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "data": {}}

@mcp.resource("resource://webhook_subscriptions")
async def get_webhook_subscriptions_resource() -> dict:
    """Get webhook subscriptions as a resource"""
    if webhook_handler is None:
        return {"status": "error", "message": "Webhook handler not initialized", "data": []}
    
    try:
        result = await webhook_handler.get_subscriptions()
        return {
            "status": "success",
            "data": result,
            "description": "WhatsApp Webhook Subscriptions"
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "data": []}

@mcp.resource("resource://waba_accounts")
async def get_waba_accounts_resource() -> dict:
    """Get WABA accounts as a resource"""
    if business_account_handler is None:
        return {"status": "error", "message": "Business Account handler not initialized", "data": []}
    
    try:
        result = await business_account_handler.get_owned_wabas()
        return {
            "status": "success",
            "data": result,
            "description": "WhatsApp Business Accounts"
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "data": []}

if __name__ == "__main__":
    print("🚀 Starting WhatsApp Cloud API Comprehensive MCP Server...")
    print("📱 Supported features:")
    print("   • Text, media, interactive, location, contact messaging")
    print("   • Template message management and sending")
    print("   • Business profile management")
    print("   • Phone number operations")
    print("   • Media upload and management")
    print("   • Message reactions and replies")
    print("   • WhatsApp Flows (interactive experiences)")
    print("   • Analytics and metrics")
    print("   • Webhook management")
    print("   • Business account management")
    print("   • Advanced phone number operations")
    print("\n🔧 Required environment variables:")
    print("   • META_ACCESS_TOKEN (required)")
    print("   • META_PHONE_NUMBER_ID (required)")
    print("   • WABA_ID (required for flows, analytics, webhooks)")
    print("   • META_BUSINESS_ACCOUNT_ID (required for templates)")
    print("   • META_BUSINESS_PORTFOLIO_ID (optional, for business account management)")
    print("   • META_APP_ID (optional, for webhook management)")
    print("\n▶️  Starting server...")
    
    mcp.run(transport='stdio')