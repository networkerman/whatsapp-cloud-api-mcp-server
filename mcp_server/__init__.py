"""
MCP Server package for comprehensive WhatsApp Cloud API operations.
"""

# Legacy imports for backward compatibility
from .whatsapp_handler import WhatsAppHandler, WhatsAppMessage

# New comprehensive handlers
from .base_handler import BaseWhatsAppHandler
from .messaging_handler import MessagingHandler
from .template_handler import TemplateHandler
from .business_handler import BusinessHandler
from .media_handler import MediaHandler

# Models
from .models import (
    WhatsAppMessageRequest, MessageType, InteractiveType,
    TemplateObject, TemplateComponent, TemplateParameter,
    MediaObject, LocationObject, ContactObject, InteractiveObject,
    MessageTemplate, TemplateCategory, BusinessProfile,
    ApiResponse, MessageResponse
)

__all__ = [
    # Legacy
    'WhatsAppHandler', 'WhatsAppMessage',
    
    # Handlers
    'BaseWhatsAppHandler', 'MessagingHandler', 'TemplateHandler', 
    'BusinessHandler', 'MediaHandler',
    
    # Models
    'WhatsAppMessageRequest', 'MessageType', 'InteractiveType',
    'TemplateObject', 'TemplateComponent', 'TemplateParameter',
    'MediaObject', 'LocationObject', 'ContactObject', 'InteractiveObject',
    'MessageTemplate', 'TemplateCategory', 'BusinessProfile',
    'ApiResponse', 'MessageResponse'
] 