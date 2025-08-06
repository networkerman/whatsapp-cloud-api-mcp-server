#!/usr/bin/env python3
"""
Claude MCP Client for WhatsApp Cloud API
Connects Claude to your deployed WhatsApp API server via HTTP
"""

import asyncio
import json
import sys
from typing import Any, Dict, List
import httpx
from mcp.server.fastmcp import FastMCP

# Your Railway deployment URL
WHATSAPP_API_BASE_URL = "https://whatsapp-cloud-api-mcp-server-production.up.railway.app"

class WhatsAppClaudeClient:
    """MCP client that bridges Claude to your deployed WhatsApp API"""
    
    def __init__(self):
        self.base_url = WHATSAPP_API_BASE_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def send_text_message(self, phone_number: str, message: str, preview_url: bool = False) -> Dict[str, Any]:
        """Send a text message via your deployed WhatsApp API"""
        url = f"{self.base_url}/api/v1/messaging/send-text"
        payload = {
            "phone_number": phone_number,
            "message": message,
            "preview_url": preview_url
        }
        
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def send_template_message(self, phone_number: str, template_name: str, 
                                  language_code: str, body_parameters: List[str] = None) -> Dict[str, Any]:
        """Send a template message via your deployed WhatsApp API"""
        url = f"{self.base_url}/api/v1/templates/send"
        payload = {
            "phone_number": phone_number,
            "template_name": template_name,
            "language_code": language_code,
            "body_parameters": body_parameters or []
        }
        
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def get_templates(self) -> Dict[str, Any]:
        """Get available templates from your deployed WhatsApp API"""
        url = f"{self.base_url}/api/v1/templates/"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def get_business_profile(self) -> Dict[str, Any]:
        """Get business profile from your deployed WhatsApp API"""
        url = f"{self.base_url}/api/v1/business/profile"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

# Create MCP server for Claude
mcp = FastMCP(title="WhatsApp Cloud API Client for Claude")
whatsapp_client = WhatsAppClaudeClient()

@mcp.tool()
async def send_whatsapp_text(phone_number: str, message: str, preview_url: bool = False) -> dict:
    """
    Send a WhatsApp text message to a phone number.
    
    Args:
        phone_number: Phone number with country code (e.g., +919823329163)
        message: Text message to send
        preview_url: Whether to show URL previews (default: False)
    
    Returns:
        dict: Response with status and message details
    """
    return await whatsapp_client.send_text_message(phone_number, message, preview_url)

@mcp.tool()
async def send_whatsapp_template(phone_number: str, template_name: str, 
                               language_code: str = "en_US", 
                               body_parameters: list = None) -> dict:
    """
    Send a WhatsApp template message to a phone number.
    
    Args:
        phone_number: Phone number with country code (e.g., +919823329163)
        template_name: Name of the approved template (e.g., "hello_world")
        language_code: Language code (default: "en_US")
        body_parameters: List of parameters for template variables
    
    Returns:
        dict: Response with status and message details
    """
    return await whatsapp_client.send_template_message(
        phone_number, template_name, language_code, body_parameters or []
    )

@mcp.tool()
async def get_whatsapp_templates() -> dict:
    """
    Get all available WhatsApp message templates.
    
    Returns:
        dict: List of available templates with their details
    """
    return await whatsapp_client.get_templates()

@mcp.tool()
async def get_whatsapp_business_info() -> dict:
    """
    Get WhatsApp business profile information.
    
    Returns:
        dict: Business profile details including name, description, etc.
    """
    return await whatsapp_client.get_business_profile()

@mcp.resource("resource://whatsapp-status")
async def whatsapp_server_status() -> dict:
    """Get the status of your deployed WhatsApp server"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{WHATSAPP_API_BASE_URL}/")
            return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    print("🚀 Starting WhatsApp MCP Client for Claude...")
    print(f"🌐 Connected to: {WHATSAPP_API_BASE_URL}")
    print("📱 Available tools:")
    print("   • send_whatsapp_text - Send text messages")
    print("   • send_whatsapp_template - Send template messages") 
    print("   • get_whatsapp_templates - List available templates")
    print("   • get_whatsapp_business_info - Get business profile")
    print("\n🔗 Connecting to Claude...")
    
    try:
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        print("\n👋 WhatsApp MCP Client stopped")
    finally:
        asyncio.run(whatsapp_client.close())