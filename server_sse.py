#!/usr/bin/env python3
"""
WhatsApp Cloud API MCP Server - SSE Transport
Deploys the MCP server with Server-Sent Events (SSE) transport for remote access.
"""

import asyncio
import logging
import os
from mcp.server.sse import SseServerTransport
from mcp.server.session import ServerSession
from mcp.types import (
    CallToolResult,
    ListResourcesResult,
    ListToolsResult,
    ReadResourceResult,
)
from dotenv import load_dotenv

# Import your MCP handlers
from mcp_server import (
    MessagingHandler, TemplateHandler, BusinessHandler, MediaHandler,
    WhatsAppHandler
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("whatsapp-mcp-sse")

class WhatsAppMCPServer:
    def __init__(self):
        self.messaging_handler = None
        self.template_handler = None
        self.business_handler = None
        self.media_handler = None
        
        # Initialize handlers
        try:
            self.messaging_handler = MessagingHandler()
            self.template_handler = TemplateHandler()
            self.business_handler = BusinessHandler()
            self.media_handler = MediaHandler()
            logger.info("✅ All handlers initialized successfully")
        except Exception as e:
            logger.error(f"❌ Handler initialization failed: {e}")
            
    async def list_tools(self) -> ListToolsResult:
        """List all available tools."""
        tools = []
        
        # Add messaging tools
        tools.extend([
            {
                "name": "send_text_message",
                "description": "Send a text message via WhatsApp",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "phone_number": {"type": "string", "description": "Recipient phone number"},
                        "message": {"type": "string", "description": "Message text"},
                        "preview_url": {"type": "boolean", "description": "Enable URL preview"}
                    },
                    "required": ["phone_number", "message"]
                }
            },
            {
                "name": "send_template_message",
                "description": "Send a template message via WhatsApp",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "phone_number": {"type": "string", "description": "Recipient phone number"},
                        "template_name": {"type": "string", "description": "Template name"},
                        "language_code": {"type": "string", "description": "Language code (e.g., en_US)"},
                        "body_parameters": {"type": "array", "description": "Template parameters"}
                    },
                    "required": ["phone_number", "template_name", "language_code"]
                }
            }
        ])
        
        return ListToolsResult(tools=tools)
    
    async def call_tool(self, name: str, arguments: dict) -> CallToolResult:
        """Execute a tool call."""
        try:
            if name == "send_text_message":
                if not self.messaging_handler:
                    return CallToolResult(content=[{"type": "text", "text": "Messaging handler not initialized"}])
                
                result = await self.messaging_handler.send_text_message(
                    arguments["phone_number"],
                    arguments["message"],
                    arguments.get("preview_url", False)
                )
                return CallToolResult(content=[{"type": "text", "text": str(result)}])
                
            elif name == "send_template_message":
                if not self.template_handler:
                    return CallToolResult(content=[{"type": "text", "text": "Template handler not initialized"}])
                
                result = await self.template_handler.send_template_message(
                    arguments["phone_number"],
                    arguments["template_name"],
                    arguments["language_code"],
                    arguments.get("body_parameters", [])
                )
                return CallToolResult(content=[{"type": "text", "text": str(result)}])
                
            else:
                return CallToolResult(content=[{"type": "text", "text": f"Unknown tool: {name}"}])
                
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return CallToolResult(content=[{"type": "text", "text": f"Error: {str(e)}"}])
    
    async def list_resources(self) -> ListResourcesResult:
        """List available resources."""
        resources = [
            {
                "uri": "resource://contacts",
                "name": "Sample Contacts",
                "description": "List of sample contacts"
            },
            {
                "uri": "resource://templates",
                "name": "Message Templates",
                "description": "Available WhatsApp message templates"
            }
        ]
        return ListResourcesResult(resources=resources)
    
    async def read_resource(self, uri: str) -> ReadResourceResult:
        """Read a specific resource."""
        if uri == "resource://contacts":
            contacts = [
                {"name": "João da Silva", "phone_number": "+55629999999999"},
                {"name": "Test Contact", "phone_number": "+1234567890"},
            ]
            return ReadResourceResult(contents=[{"type": "text", "text": str(contacts)}])
        
        elif uri == "resource://templates":
            if self.template_handler:
                templates = await self.template_handler.get_message_templates()
                return ReadResourceResult(contents=[{"type": "text", "text": str(templates)}])
            else:
                return ReadResourceResult(contents=[{"type": "text", "text": "Template handler not initialized"}])
        
        else:
            return ReadResourceResult(contents=[{"type": "text", "text": f"Resource not found: {uri}"}])

async def main():
    # Validate environment variables
    required_vars = ["META_ACCESS_TOKEN", "META_PHONE_NUMBER_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {missing_vars}")
        return
    
    # Create server instance
    server = WhatsAppMCPServer()
    
    # Create transport
    host = os.getenv("MCP_SERVER_HOST", "localhost")
    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    
    logger.info(f"🚀 Starting WhatsApp MCP Server with SSE transport")
    logger.info(f"🌐 Server will be available at: http://{host}:{port}")
    logger.info(f"📡 SSE endpoint: http://{host}:{port}/sse")
    
    # Start server
    transport = SseServerTransport(host=host, port=port)
    
    async with transport.run_server() as server_transport:
        session = ServerSession(server_transport, {
            "list_tools": server.list_tools,
            "call_tool": server.call_tool,
            "list_resources": server.list_resources,
            "read_resource": server.read_resource,
        })
        
        logger.info("✅ Server started successfully!")
        logger.info("🔗 Connect your MCP client to the SSE endpoint")
        
        try:
            await session.run()
        except KeyboardInterrupt:
            logger.info("🛑 Server stopped by user")
        except Exception as e:
            logger.error(f"❌ Server error: {e}")

if __name__ == "__main__":
    asyncio.run(main())