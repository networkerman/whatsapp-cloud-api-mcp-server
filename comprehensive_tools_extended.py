"""
Enhanced Comprehensive WhatsApp Cloud API tools for MCP Server with advanced validation.
This file contains all the tool definitions with enhanced validation and constraint handling.
"""

from typing import List, Dict, Any, Optional

def register_comprehensive_tools_extended(mcp, messaging_handler, template_handler, business_handler, media_handler):
    """Register all comprehensive WhatsApp Cloud API tools with enhanced validation"""
    
    # ================================
    # TEXT MESSAGING TOOLS
    # ================================

    @mcp.tool()
    async def send_text_message(
        phone_number: str, 
        message: str, 
        preview_url: bool = False,
        reply_to_message_id: Optional[str] = None
    ) -> dict:
        """
        Send a text message with advanced options.
        
        Args:
            phone_number: Recipient phone number with country code
            message: Text message content
            preview_url: Whether to show URL previews
            reply_to_message_id: ID of message to reply to (optional)
            
        Returns:
            dict: Response with message status and ID
        """
        try:
            return await messaging_handler.send_text_message(
                phone_number, message, preview_url, reply_to_message_id
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def send_reaction(phone_number: str, message_id: str, emoji: str) -> dict:
        """
        React to a message with an emoji.
        
        Args:
            phone_number: Recipient phone number
            message_id: ID of the message to react to
            emoji: Emoji to use for reaction (use empty string to remove)
            
        Returns:
            dict: Response with reaction status
        """
        try:
            return await messaging_handler.send_reaction_message(phone_number, message_id, emoji)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ================================
    # ENHANCED TEMPLATE MANAGEMENT TOOLS
    # ================================

    @mcp.tool()
    async def get_message_templates(
        name: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
        language: Optional[str] = None,
        limit: int = 100
    ) -> dict:
        """
        Get message templates with optional filtering.
        
        Args:
            name: Filter by template name
            status: Filter by template status (APPROVED, PENDING, REJECTED)
            category: Filter by category (MARKETING, UTILITY, AUTHENTICATION)
            language: Filter by language code
            limit: Maximum number of templates to return
            
        Returns:
            dict: List of message templates
        """
        try:
            return await template_handler.get_message_templates(name, status, category, language, limit)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def create_message_template_enhanced(
        name: str,
        category: str,
        language: str,
        body_text: str,
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None,
        buttons: Optional[List[Dict[str, str]]] = None,
        example_values: Optional[Dict[str, List[str]]] = None
    ) -> dict:
        """
        Create a new message template with comprehensive validation and enhanced constraints.
        
        Args:
            name: Template name (lowercase, numbers, underscores only, max 512 chars)
            category: Template category (MARKETING, UTILITY, AUTHENTICATION)
            language: Language code (e.g., en_US, es_ES)
            body_text: Main message text (550 chars max, max 10 emojis total, format: *bold*, _italic_, ~strike~, ```mono```, no \n\n)
            header_text: Optional header text (60 chars max)
            footer_text: Optional footer text (60 chars max)
            buttons: Optional list of button objects (max 20 chars each, plain text only)
            example_values: Optional example values for variables {{1}}, {{2}}, etc.
            
        Returns:
            dict: Template creation response with detailed validation results
        """
        try:
            # Build components list with enhanced validation
            components = []
            
            # Add header if provided
            if header_text:
                components.append({
                    "type": "HEADER",
                    "format": "TEXT",
                    "text": header_text
                })
            
            # Add body (required)
            body_component = {
                "type": "BODY",
                "text": body_text
            }
            
            # Add example values if provided
            if example_values and "body" in example_values:
                body_component["example"] = {
                    "body_text": example_values["body"]
                }
            
            components.append(body_component)
            
            # Add footer if provided
            if footer_text:
                components.append({
                    "type": "FOOTER",
                    "text": footer_text
                })
            
            # Add buttons if provided
            if buttons:
                components.append({
                    "type": "BUTTONS",
                    "buttons": buttons
                })
            
            return await template_handler.create_message_template(
                name, category, language, components
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def create_carousel_template_enhanced(
        name: str,
        category: str,
        language: str,
        body_text: str,
        cards: List[Dict[str, Any]]
    ) -> dict:
        """
        Create a carousel template with comprehensive validation and enhanced constraints.
        
        Args:
            name: Template name (lowercase, numbers, underscores only, max 512 chars)
            category: Template category (MARKETING, UTILITY, AUTHENTICATION)
            language: Language code (e.g., en_US, es_ES)
            body_text: Main message text (550 chars max, max 10 emojis total)
            cards: List of carousel cards (2-10 cards, identical structure required)
                Each card should have:
                - body_text: Card body text
                - header: Optional header object with format and example
                - buttons: Optional list of button objects (max 2 per card)
                
        Returns:
            dict: Template creation response with detailed validation results
        """
        try:
            return await template_handler.create_carousel_template(
                name, category, language, body_text, cards
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def create_authentication_template(
        name: str,
        language: str,
        verification_code_text: str = "{{1}} is your verification code"
    ) -> dict:
        """
        Create an authentication template with proper format validation.
        
        Args:
            name: Template name (lowercase, numbers, underscores only, max 512 chars)
            language: Language code (e.g., en_US, es_ES)
            verification_code_text: Text starting with {{1}} is your verification code
            
        Returns:
            dict: Template creation response with validation results
        """
        try:
            # Validate authentication format
            if not verification_code_text.startswith("{{1}} is your verification code"):
                return {
                    "success": False,
                    "validation_errors": [
                        {
                            "field": "verification_code_text",
                            "message": "Authentication template must start with '{{1}} is your verification code'"
                        }
                    ]
                }
            
            components = [{
                "type": "BODY",
                "text": verification_code_text
            }]
            
            return await template_handler.create_message_template(
                name, "AUTHENTICATION", language, components
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def create_template_with_media_header(
        name: str,
        category: str,
        language: str,
        body_text: str,
        header_format: str,  # IMAGE, VIDEO, DOCUMENT
        header_example_url: str,
        buttons: Optional[List[Dict[str, str]]] = None
    ) -> dict:
        """
        Create a template with media header and comprehensive validation.
        
        Args:
            name: Template name (lowercase, numbers, underscores only, max 512 chars)
            category: Template category (MARKETING, UTILITY, AUTHENTICATION)
            language: Language code (e.g., en_US, es_ES)
            body_text: Main message text (550 chars max, max 10 emojis total)
            header_format: Media format (IMAGE, VIDEO, DOCUMENT)
            header_example_url: Example media URL (must be HTTPS)
            buttons: Optional list of button objects (max 20 chars each, plain text only)
            
        Returns:
            dict: Template creation response with validation results
        """
        try:
            components = []
            
            # Add media header
            components.append({
                "type": "HEADER",
                "format": header_format,
                "example": {
                    "header_url": [header_example_url]
                }
            })
            
            # Add body (required)
            components.append({
                "type": "BODY",
                "text": body_text
            })
            
            # Add buttons if provided
            if buttons:
                components.append({
                    "type": "BUTTONS",
                    "buttons": buttons
                })
            
            return await template_handler.create_message_template(
                name, category, language, components
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def validate_template_data(
        name: str,
        category: str,
        language: str,
        body_text: str,
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None,
        buttons: Optional[List[Dict[str, str]]] = None
    ) -> dict:
        """
        Validate template data without creating the template.
        
        Args:
            name: Template name to validate
            category: Template category to validate
            language: Language code to validate
            body_text: Body text to validate
            header_text: Optional header text to validate
            footer_text: Optional footer text to validate
            buttons: Optional buttons to validate
            
        Returns:
            dict: Validation results with detailed error messages
        """
        try:
            from .validation import (
                validateTemplateName, validateTemplateCategory, validateLanguageCode,
                validateCharacterLimits, validateEmojiLimit, validateFormatting,
                validateButtonText, validateUrls, validatePhoneNumbers,
                formatValidationErrors, ValidationResult
            )
            
            errors = []
            
            # Validate basic fields
            name_validation = validateTemplateName(name)
            if not name_validation.isValid:
                errors.append(name_validation.error)
            
            category_validation = validateTemplateCategory(category)
            if not category_validation.isValid:
                errors.append(category_validation.error)
            
            language_validation = validateLanguageCode(language)
            if not language_validation.isValid:
                errors.append(language_validation.error)
            
            # Validate text content
            all_text = [body_text]
            if header_text:
                all_text.append(header_text)
            if footer_text:
                all_text.append(footer_text)
            
            # Validate character limits
            body_validation = validateCharacterLimits('body', body_text)
            if not body_validation.isValid:
                errors.append(body_validation.error)
            
            if header_text:
                header_validation = validateCharacterLimits('header', header_text)
                if not header_validation.isValid:
                    errors.append(header_validation.error)
            
            if footer_text:
                footer_validation = validateCharacterLimits('footer', footer_text)
                if not footer_validation.isValid:
                    errors.append(footer_validation.error)
            
            # Validate emoji limit
            emoji_validation = validateEmojiLimit(all_text)
            if not emoji_validation.isValid:
                errors.append(emoji_validation.error)
            
            # Validate formatting
            for text in all_text:
                format_validation = validateFormatting(text)
                if not format_validation.isValid and format_validation.errors:
                    errors.extend(format_validation.errors)
            
            # Validate buttons
            if buttons:
                button_validation = validateButtonText(buttons)
                if not button_validation.isValid:
                    errors.append(button_validation.error)
                
                url_validation = validateUrls(buttons)
                if not url_validation.isValid:
                    errors.append(url_validation.error)
                
                phone_validation = validatePhoneNumbers(buttons)
                if not phone_validation.isValid:
                    errors.append(phone_validation.error)
            
            # Validate authentication format if applicable
            if category.upper() == 'AUTHENTICATION':
                from .validation import validateAuthenticationFormat
                auth_validation = validateAuthenticationFormat(body_text)
                if not auth_validation.isValid:
                    errors.append(auth_validation.error)
            
            if errors:
                return {
                    "success": False,
                    "validation_errors": [
                        {
                            "field": "template",
                            "message": error
                        }
                        for error in errors
                    ]
                }
            
            return {
                "success": True,
                "message": "Template data is valid and ready for creation"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def send_template_message(
        phone_number: str,
        template_name: str,
        language_code: str = "en_US",
        body_parameters: Optional[List[str]] = None,
        header_parameters: Optional[List[str]] = None,
        reply_to_message_id: Optional[str] = None
    ) -> dict:
        """
        Send a template message with text parameters.
        
        Args:
            phone_number: Recipient phone number
            template_name: Name of the approved template
            language_code: Language code
            body_parameters: List of parameters for template body
            header_parameters: List of parameters for template header
            reply_to_message_id: ID of message to reply to
            
        Returns:
            dict: Response with message status
        """
        try:
            return await template_handler.send_template_with_text_parameters(
                phone_number, template_name, language_code, header_parameters, body_parameters, reply_to_message_id
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def delete_message_template(template_name: str) -> dict:
        """
        Delete a message template.
        
        Args:
            template_name: Name of the template to delete
            
        Returns:
            dict: Deletion response
        """
        try:
            return await template_handler.delete_message_template(template_name)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ================================
    # MEDIA MESSAGING TOOLS
    # ================================

    @mcp.tool()
    async def send_template_with_media_header(
        phone_number: str,
        template_name: str,
        language_code: str,
        media_type: str,
        media_url: Optional[str] = None,
        media_id: Optional[str] = None,
        body_parameters: Optional[List[str]] = None,
        reply_to_message_id: Optional[str] = None
    ) -> dict:
        """
        Send a template message with media in the header.
        
        Args:
            phone_number: Recipient phone number
            template_name: Name of the approved template
            language_code: Language code
            media_type: Type of media (image, video, document)
            media_url: URL of the media file
            media_id: ID of uploaded media
            body_parameters: List of parameters for template body
            reply_to_message_id: ID of message to reply to
            
        Returns:
            dict: Response with message status
        """
        try:
            return await template_handler.send_template_with_media_header(
                phone_number, template_name, language_code, media_type, media_id, media_url, body_parameters, reply_to_message_id
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def send_image_message(
        phone_number: str,
        image_url: Optional[str] = None,
        image_id: Optional[str] = None,
        caption: Optional[str] = None,
        reply_to_message_id: Optional[str] = None
    ) -> dict:
        """
        Send an image message.
        
        Args:
            phone_number: Recipient phone number
            image_url: URL of the image
            image_id: ID of uploaded image
            caption: Optional caption for the image
            reply_to_message_id: ID of message to reply to
            
        Returns:
            dict: Response with message status
        """
        try:
            return await messaging_handler.send_image_message(
                phone_number, image_url, image_id, caption, reply_to_message_id
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def send_video_message(
        phone_number: str,
        video_url: Optional[str] = None,
        video_id: Optional[str] = None,
        caption: Optional[str] = None,
        reply_to_message_id: Optional[str] = None
    ) -> dict:
        """
        Send a video message.
        
        Args:
            phone_number: Recipient phone number
            video_url: URL of the video
            video_id: ID of uploaded video
            caption: Optional caption for the video
            reply_to_message_id: ID of message to reply to
            
        Returns:
            dict: Response with message status
        """
        try:
            return await messaging_handler.send_video_message(
                phone_number, video_url, video_id, caption, reply_to_message_id
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def send_document_message(
        phone_number: str,
        document_url: Optional[str] = None,
        document_id: Optional[str] = None,
        filename: Optional[str] = None,
        caption: Optional[str] = None,
        reply_to_message_id: Optional[str] = None
    ) -> dict:
        """
        Send a document message.
        
        Args:
            phone_number: Recipient phone number
            document_url: URL of the document
            document_id: ID of uploaded document
            filename: Optional filename for the document
            caption: Optional caption for the document
            reply_to_message_id: ID of message to reply to
            
        Returns:
            dict: Response with message status
        """
        try:
            return await messaging_handler.send_document_message(
                phone_number, document_url, document_id, filename, caption, reply_to_message_id
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ================================
    # INTERACTIVE MESSAGING TOOLS
    # ================================

    @mcp.tool()
    async def send_button_message(
        phone_number: str,
        body_text: str,
        buttons: List[Dict[str, str]],
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None,
        reply_to_message_id: Optional[str] = None
    ) -> dict:
        """
        Send an interactive button message.
        
        Args:
            phone_number: Recipient phone number
            body_text: Main message text
            buttons: List of button objects [{"type": "QUICK_REPLY", "text": "Button Text"}]
            header_text: Optional header text
            footer_text: Optional footer text
            reply_to_message_id: ID of message to reply to
            
        Returns:
            dict: Response with message status
        """
        try:
            return await messaging_handler.send_button_message(
                phone_number, body_text, buttons, header_text, footer_text, reply_to_message_id
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def send_list_message(
        phone_number: str,
        body_text: str,
        button_text: str,
        sections: List[Dict[str, Any]],
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None,
        reply_to_message_id: Optional[str] = None
    ) -> dict:
        """
        Send an interactive list message.
        
        Args:
            phone_number: Recipient phone number
            body_text: Main message text
            button_text: Text for the list button
            sections: List of sections with rows
            header_text: Optional header text
            footer_text: Optional footer text
            reply_to_message_id: ID of message to reply to
            
        Returns:
            dict: Response with message status
        """
        try:
            return await messaging_handler.send_list_message(
                phone_number, body_text, button_text, sections, header_text, footer_text, reply_to_message_id
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ================================
    # LOCATION AND CONTACT TOOLS
    # ================================

    @mcp.tool()
    async def send_location_message(
        phone_number: str,
        latitude: float,
        longitude: float,
        name: Optional[str] = None,
        address: Optional[str] = None,
        reply_to_message_id: Optional[str] = None
    ) -> dict:
        """
        Send a location message.
        
        Args:
            phone_number: Recipient phone number
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            name: Optional location name
            address: Optional location address
            reply_to_message_id: ID of message to reply to
            
        Returns:
            dict: Response with message status
        """
        try:
            return await messaging_handler.send_location_message(
                phone_number, latitude, longitude, name, address, reply_to_message_id
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def send_contact_message(
        phone_number: str,
        contact_name: str,
        contact_phone: Optional[str] = None,
        contact_email: Optional[str] = None,
        reply_to_message_id: Optional[str] = None
    ) -> dict:
        """
        Send a contact message.
        
        Args:
            phone_number: Recipient phone number
            contact_name: Name of the contact
            contact_phone: Phone number of the contact
            contact_email: Email of the contact
            reply_to_message_id: ID of message to reply to
            
        Returns:
            dict: Response with message status
        """
        try:
            return await messaging_handler.send_contact_message(
                phone_number, contact_name, contact_phone, contact_email, reply_to_message_id
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ================================
    # MEDIA MANAGEMENT TOOLS
    # ================================

    @mcp.tool()
    async def upload_media(file_path: str, media_type: str = "auto") -> dict:
        """
        Upload media file to WhatsApp.
        
        Args:
            file_path: Path to the media file
            media_type: Type of media (auto, image, video, audio, document)
            
        Returns:
            dict: Response with media ID
        """
        try:
            return await media_handler.upload_media(file_path, media_type)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def get_media_info(media_id: str) -> dict:
        """
        Get information about uploaded media.
        
        Args:
            media_id: ID of the media
            
        Returns:
            dict: Media information
        """
        try:
            return await media_handler.get_media_info(media_id)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ================================
    # BUSINESS MANAGEMENT TOOLS
    # ================================

    @mcp.tool()
    async def get_business_profile() -> dict:
        """
        Get business profile information.
        
        Returns:
            dict: Business profile data
        """
        try:
            return await business_handler.get_business_profile()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def get_phone_numbers() -> dict:
        """
        Get list of phone numbers associated with the business account.
        
        Returns:
            dict: List of phone numbers with details
        """
        try:
            return await business_handler.get_phone_numbers()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mark_message_as_read(message_id: str) -> dict:
        """
        Mark a message as read.
        
        Args:
            message_id: ID of the message to mark as read
            
        Returns:
            dict: Response with read status
        """
        try:
            return await messaging_handler.mark_message_as_read(message_id)
        except Exception as e:
            return {"status": "error", "message": str(e)} 