"""
WhatsApp Webhook Handler for MCP Server.
Handles all WhatsApp webhook subscription and management operations.
"""

import os
import aiohttp
import json
from typing import Dict, Any, Optional, List
from .base_handler import BaseWhatsAppHandler


class WebhookHandler(BaseWhatsAppHandler):
    """Handler for WhatsApp Webhook operations."""
    
    def __init__(self):
        super().__init__()
        # Validate WABA ID is available for webhook operations
        if not (self.waba_id or self.business_account_id):
            raise ValueError("Either WABA_ID or META_BUSINESS_ACCOUNT_ID environment variable is required for webhook operations")
        
        # Use WABA_ID for webhook operations (fallback to business_account_id)
        waba_for_operations = self.waba_id or self.business_account_id
        self.subscribed_apps_url = f"{self.base_url}/{waba_for_operations}/subscribed_apps"
    
    async def subscribe_to_waba(self) -> Dict[str, Any]:
        """
        Subscribe your app to a WABA to receive webhook events.
        
        Returns:
            dict: Subscription response
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.subscribed_apps_url,
                headers=self._prepare_headers()
            ) as response:
                return await self._handle_response(response, "Subscribe to WABA")
    
    async def get_subscriptions(self) -> Dict[str, Any]:
        """
        Get all subscriptions for a WABA.
        
        Returns:
            dict: List of subscriptions
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.subscribed_apps_url,
                headers=self._prepare_headers()
            ) as response:
                return await self._handle_response(response, "Get subscriptions")
    
    async def unsubscribe_from_waba(self) -> Dict[str, Any]:
        """
        Unsubscribe your app from a WABA.
        
        Returns:
            dict: Unsubscription response
        """
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                self.subscribed_apps_url,
                headers=self._prepare_headers()
            ) as response:
                return await self._handle_response(response, "Unsubscribe from WABA")
    
    async def override_callback_url(self, callback_url: str) -> Dict[str, Any]:
        """
        Override the callback URL for webhook events.
        
        Args:
            callback_url: New callback URL for webhook events
            
        Returns:
            dict: Override response
        """
        payload = {
            "callback_url": callback_url
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.subscribed_apps_url,
                headers=self._prepare_headers(),
                json=payload
            ) as response:
                return await self._handle_response(response, "Override callback URL")
    
    async def get_webhook_verification_token(self) -> Dict[str, Any]:
        """
        Get webhook verification token for the app.
        
        Returns:
            dict: Verification token information
        """
        url = f"{self.base_url}/{os.getenv('META_APP_ID')}"
        params = {
            "fields": "webhook_verification_token"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers=self._prepare_headers(),
                params=params
            ) as response:
                return await self._handle_response(response, "Get webhook verification token")
    
    async def set_webhook_verification_token(self, verification_token: str) -> Dict[str, Any]:
        """
        Set webhook verification token for the app.
        
        Args:
            verification_token: Verification token to set
            
        Returns:
            dict: Set token response
        """
        url = f"{self.base_url}/{os.getenv('META_APP_ID')}"
        payload = {
            "webhook_verification_token": verification_token
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=self._prepare_headers(),
                json=payload
            ) as response:
                return await self._handle_response(response, "Set webhook verification token")
    
    async def get_webhook_fields(self) -> Dict[str, Any]:
        """
        Get webhook fields for the app.
        
        Returns:
            dict: Webhook fields information
        """
        url = f"{self.base_url}/{os.getenv('META_APP_ID')}"
        params = {
            "fields": "webhook_fields"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers=self._prepare_headers(),
                params=params
            ) as response:
                return await self._handle_response(response, "Get webhook fields")
    
    async def set_webhook_fields(self, fields: List[str]) -> Dict[str, Any]:
        """
        Set webhook fields for the app.
        
        Args:
            fields: List of webhook fields to set
            
        Returns:
            dict: Set fields response
        """
        url = f"{self.base_url}/{os.getenv('META_APP_ID')}"
        payload = {
            "webhook_fields": fields
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=self._prepare_headers(),
                json=payload
            ) as response:
                return await self._handle_response(response, "Set webhook fields")
    
    async def _handle_response(self, response, operation_name: str) -> Dict[str, Any]:
        """Handle API response"""
        try:
            if response.status == 200:
                data = await response.json()
                return {
                    "status": "success",
                    "data": data,
                    "operation": operation_name
                }
            else:
                error_data = await response.json()
                return {
                    "status": "error",
                    "error": error_data.get("error", {}).get("message", f"Failed to {operation_name}"),
                    "operation": operation_name,
                    "status_code": response.status
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "operation": operation_name
            } 