"""
WhatsApp Flows Handler for MCP Server.
Handles all WhatsApp Flow operations including create, list, get, update, publish, and migrate flows.
"""

import os
import aiohttp
import json
from typing import Dict, Any, Optional, List
from .base_handler import BaseWhatsAppHandler


class FlowHandler(BaseWhatsAppHandler):
    """Handler for WhatsApp Flow operations."""
    
    def __init__(self):
        super().__init__()
        # Validate WABA ID is available for flow operations
        if not (self.waba_id or self.business_account_id):
            raise ValueError("Either WABA_ID or META_BUSINESS_ACCOUNT_ID environment variable is required for flow operations")
        
        # Use WABA_ID for flow operations (fallback to business_account_id)
        waba_for_operations = self.waba_id or self.business_account_id
        self.flows_url = f"{self.base_url}/{waba_for_operations}/flows"
        self.migrate_flows_url = f"{self.base_url}/{waba_for_operations}/migrate_flows"
    
    async def create_flow(
        self, 
        name: str, 
        categories: List[str],
        clone_flow_id: Optional[str] = None,
        endpoint_uri: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new WhatsApp Flow.
        
        Args:
            name: Name of the flow
            categories: List of flow categories (SIGN_UP, SIGN_IN, APPOINTMENT_BOOKING, CONTACT_US, OTHER)
            clone_flow_id: Optional ID of existing flow to clone
            endpoint_uri: Optional endpoint URI for the flow
            
        Returns:
            dict: Response with flow details
        """
        payload = {
            "name": name,
            "categories": categories
        }
        
        if clone_flow_id:
            payload["clone_flow_id"] = clone_flow_id
        if endpoint_uri:
            payload["endpoint_uri"] = endpoint_uri
            
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.flows_url,
                headers=self.headers,
                json=payload
            ) as response:
                return await self._handle_response(response, "Create flow")
    
    async def list_flows(self, limit: int = 100) -> Dict[str, Any]:
        """
        List all flows for the WABA.
        
        Args:
            limit: Maximum number of flows to return
            
        Returns:
            dict: List of flows
        """
        params = {"limit": limit}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.flows_url,
                headers=self.headers,
                params=params
            ) as response:
                return await self._handle_response(response, "List flows")
    
    async def get_flow(self, flow_id: str) -> Dict[str, Any]:
        """
        Get details of a specific flow.
        
        Args:
            flow_id: ID of the flow to retrieve
            
        Returns:
            dict: Flow details
        """
        url = f"{self.base_url}/{flow_id}"
        params = {
            "fields": "id,name,categories,preview,status,validation_errors,json_version,data_api_version,data_channel_uri,health_status,whatsapp_business_account,application"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers=self.headers,
                params=params
            ) as response:
                return await self._handle_response(response, "Get flow")
    
    async def update_flow(self, flow_id: str, name: Optional[str] = None, categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Update a flow's name or categories.
        
        Args:
            flow_id: ID of the flow to update
            name: New name for the flow
            categories: New categories for the flow
            
        Returns:
            dict: Updated flow details
        """
        url = f"{self.base_url}/{flow_id}"
        payload = {}
        
        if name:
            payload["name"] = name
        if categories:
            payload["categories"] = categories
            
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=self.headers,
                json=payload
            ) as response:
                return await self._handle_response(response, "Update flow")
    
    async def publish_flow(self, flow_id: str) -> Dict[str, Any]:
        """
        Publish a flow (makes it immutable).
        
        Args:
            flow_id: ID of the flow to publish
            
        Returns:
            dict: Published flow details
        """
        url = f"{self.base_url}/{flow_id}/publish"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=self.headers
            ) as response:
                return await self._handle_response(response, "Publish flow")
    
    async def upload_flow_json(self, flow_id: str, flow_json_content: str) -> Dict[str, Any]:
        """
        Upload flow JSON content to a flow.
        
        Args:
            flow_id: ID of the flow
            flow_json_content: JSON content of the flow
            
        Returns:
            dict: Upload response with validation errors if any
        """
        url = f"{self.base_url}/{flow_id}/assets"
        
        # Create form data with the JSON file
        data = aiohttp.FormData()
        data.add_field('flow.json', flow_json_content, filename='flow.json', content_type='application/json')
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=self.headers,
                data=data
            ) as response:
                return await self._handle_response(response, "Upload flow JSON")
    
    async def get_flow_preview(self, flow_id: str, invalidate: bool = False) -> Dict[str, Any]:
        """
        Get preview URL for a flow.
        
        Args:
            flow_id: ID of the flow
            invalidate: Whether to invalidate existing preview
            
        Returns:
            dict: Preview URL and expiry information
        """
        url = f"{self.base_url}/{flow_id}"
        params = {
            "fields": f"preview.invalidate({str(invalidate).lower()})"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers=self.headers,
                params=params
            ) as response:
                return await self._handle_response(response, "Get flow preview")
    
    async def migrate_flows(
        self, 
        source_waba_id: str, 
        source_flow_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Migrate flows from source WABA to current WABA.
        
        Args:
            source_waba_id: ID of the source WABA
            source_flow_names: Optional list of flow names to migrate
            
        Returns:
            dict: Migration results
        """
        payload = {
            "source_waba_id": source_waba_id
        }
        
        if source_flow_names:
            payload["source_flow_names"] = source_flow_names
            
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.migrate_flows_url,
                headers=self.headers,
                json=payload
            ) as response:
                return await self._handle_response(response, "Migrate flows")
    
    async def get_flow_metrics(
        self, 
        flow_id: str, 
        metric_name: str = "ENDPOINT_REQUEST_COUNT",
        granularity: str = "DAY",
        since: str = None,
        until: str = None
    ) -> Dict[str, Any]:
        """
        Get metrics for a specific flow.
        
        Args:
            flow_id: ID of the flow
            metric_name: Name of the metric (ENDPOINT_REQUEST_COUNT, ENDPOINT_REQUEST_ERROR)
            granularity: Granularity of the metrics (DAY, HOUR, MONTH)
            since: Start date (YYYY-MM-DD format)
            until: End date (YYYY-MM-DD format)
            
        Returns:
            dict: Flow metrics data
        """
        url = f"{self.base_url}/{flow_id}"
        
        # Build the fields parameter
        fields_parts = [f"metric.name({metric_name})", f"granularity({granularity})"]
        if since:
            fields_parts.append(f"since({since})")
        if until:
            fields_parts.append(f"until({until})")
            
        params = {
            "fields": ".".join(fields_parts)
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers=self.headers,
                params=params
            ) as response:
                return await self._handle_response(response, "Get flow metrics") 