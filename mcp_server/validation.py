"""
Comprehensive validation functions for WhatsApp Business API template creation.
This module provides validation functions to prevent common template creation errors.
"""

import re
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Result of a validation check"""
    isValid: bool
    error: Optional[str] = None
    errors: Optional[List[str]] = None

def validateCharacterLimits(component: str, text: str) -> ValidationResult:
    """
    Validate character limits for different template components.
    
    Args:
        component: Component type ('body', 'header', 'footer', 'button')
        text: Text to validate
        
    Returns:
        ValidationResult with validation status and error message
    """
    limits = {
        'body': 550,
        'header': 60,
        'footer': 60,
        'button': 20
    }
    
    limit = limits.get(component)
    if limit is None:
        return ValidationResult(False, f"Unknown component type: {component}")
    
    if len(text) > limit:
        return ValidationResult(
            False, 
            f"{component} exceeds {limit} character limit ({len(text)} characters)"
        )
    
    return ValidationResult(True)

def countEmojis(text: str) -> int:
    """
    Count emojis in text using Unicode emoji regex.
    
    Args:
        text: Text to count emojis in
        
    Returns:
        Number of emojis found
    """
    # Use a more compatible emoji regex pattern
    emojiRegex = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+', re.UNICODE)
    return len(emojiRegex.findall(text))

def validateEmojiLimit(allTemplateText: List[str]) -> ValidationResult:
    """
    Validate total emoji count across all template text.
    
    Args:
        allTemplateText: List of all text strings in the template
        
    Returns:
        ValidationResult with validation status and error message
    """
    totalEmojis = sum(countEmojis(text) for text in allTemplateText)
    
    if totalEmojis > 10:
        return ValidationResult(
            False,
            f"Template has {totalEmojis} emojis, maximum 10 allowed"
        )
    
    return ValidationResult(True)

def validateFormatting(text: str) -> ValidationResult:
    """
    Validate text formatting syntax.
    
    Args:
        text: Text to validate formatting in
        
    Returns:
        ValidationResult with validation status and error messages
    """
    errors = []
    
    # Check for consecutive line breaks
    if '\n\n' in text:
        errors.append('Consecutive line breaks (\\n\\n) not allowed')
    
    # Check for proper bold formatting
    boldPattern = re.compile(r'\*[^*]*\*[^*]*\*')
    validBoldPattern = re.compile(r'\*[^*]+\*')
    if boldPattern.search(text) and not validBoldPattern.search(text):
        errors.append('Invalid bold formatting - use *text*')
    
    # Check for proper italic formatting
    italicPattern = re.compile(r'_[^_]*_[^_]*_')
    validItalicPattern = re.compile(r'_[^_]+_')
    if italicPattern.search(text) and not validItalicPattern.search(text):
        errors.append('Invalid italic formatting - use _text_')
    
    # Check for proper strikethrough formatting
    strikePattern = re.compile(r'~[^~]*~[^~]*~')
    validStrikePattern = re.compile(r'~[^~]+~')
    if strikePattern.search(text) and not validStrikePattern.search(text):
        errors.append('Invalid strikethrough formatting - use ~text~')
    
    return ValidationResult(len(errors) == 0, errors=errors if errors else None)

def validateButtonCombinations(templateType: str, buttons: List[Dict[str, Any]]) -> ValidationResult:
    """
    Validate button combinations for different template types.
    
    Args:
        templateType: Type of template (e.g., 'CAROUSEL')
        buttons: List of button objects
        
    Returns:
        ValidationResult with validation status and error message
    """
    buttonTypes = [b.get('type') for b in buttons]
    
    if templateType == 'CAROUSEL':
        validCombinations = [
            ['QUICK_REPLY'],
            ['URL'],
            ['PHONE_NUMBER'],
            ['QUICK_REPLY', 'URL'],
            ['QUICK_REPLY', 'PHONE_NUMBER']
        ]
        
        isValid = any(
            len(combo) == len(buttonTypes) and 
            all(btn_type in buttonTypes for btn_type in combo)
            for combo in validCombinations
        )
        
        if not isValid:
            return ValidationResult(
                False,
                f"Invalid carousel button combination: [{', '.join(buttonTypes)}]. "
                f"Valid: [QUICK_REPLY], [URL], [PHONE_NUMBER], [QUICK_REPLY+URL], [QUICK_REPLY+PHONE_NUMBER]"
            )
    
    return ValidationResult(True)

def validateCarouselConsistency(cards: List[Dict[str, Any]]) -> ValidationResult:
    """
    Validate carousel card consistency.
    
    Args:
        cards: List of carousel card objects
        
    Returns:
        ValidationResult with validation status and error message
    """
    if len(cards) < 2 or len(cards) > 10:
        return ValidationResult(
            False,
            f"Carousel must have 2-10 cards, got {len(cards)}"
        )
    
    if not cards:
        return ValidationResult(True)
    
    firstCardStructure = {
        'hasHeader': bool(cards[0].get('header')),
        'headerType': cards[0].get('header', {}).get('format'),
        'buttonCount': len(cards[0].get('buttons', [])),
        'buttonTypes': sorted([b.get('type') for b in cards[0].get('buttons', [])])
    }
    
    for i, card in enumerate(cards[1:], 1):
        cardStructure = {
            'hasHeader': bool(card.get('header')),
            'headerType': card.get('header', {}).get('format'),
            'buttonCount': len(card.get('buttons', [])),
            'buttonTypes': sorted([b.get('type') for b in card.get('buttons', [])])
        }
        
        if cardStructure != firstCardStructure:
            return ValidationResult(
                False,
                f"Card {i + 1} structure doesn't match card 1. "
                f"All carousel cards must have identical component structure."
            )
    
    return ValidationResult(True)

def validateVariableExamples(text: str, examples: List[str]) -> ValidationResult:
    """
    Validate variable numbering and example count consistency.
    
    Args:
        text: Template text with variables
        examples: List of example values
        
    Returns:
        ValidationResult with validation status and error message
    """
    # Extract variables from text
    variablePattern = re.compile(r'\{\{(\d+)\}\}')
    variables = [int(match.group(1)) for match in variablePattern.finditer(text)]
    variables.sort()
    
    # Check sequential numbering
    expectedSequence = list(range(1, len(variables) + 1))
    if variables != expectedSequence:
        return ValidationResult(
            False,
            f"Variables must be sequential starting from {{1}}. "
            f"Found: {', '.join(f'{{{{{v}}}}}' for v in variables)}"
        )
    
    # Check example count matches variable count
    if len(variables) != len(examples):
        return ValidationResult(
            False,
            f"Variable count ({len(variables)}) doesn't match example count ({len(examples)})"
        )
    
    return ValidationResult(True)

def validateButtonText(buttons: List[Dict[str, Any]]) -> ValidationResult:
    """
    Validate button text content.
    
    Args:
        buttons: List of button objects
        
    Returns:
        ValidationResult with validation status and error message
    """
    for button in buttons:
        text = button.get('text', '')
        if not text:
            continue
        
        # Check for emojis
        if countEmojis(text) > 0:
            return ValidationResult(
                False,
                f'Button "{text}" contains emojis. Use plain text only.'
            )
        
        # Check for formatting characters
        if re.search(r'[*_~`{}]', text):
            return ValidationResult(
                False,
                f'Button "{text}" contains formatting characters. Use plain text only.'
            )
        
        # Check for line breaks
        if '\n' in text:
            return ValidationResult(
                False,
                f'Button "{text}" contains line breaks. Use plain text only.'
            )
    
    return ValidationResult(True)

def validateAuthenticationFormat(body: str) -> ValidationResult:
    """
    Validate authentication template format.
    
    Args:
        body: Template body text
        
    Returns:
        ValidationResult with validation status and error message
    """
    requiredPattern = re.compile(r'^\{\{1\}\} is your verification code')
    
    if not requiredPattern.search(body):
        return ValidationResult(
            False,
            'Authentication template must start with "{{1}} is your verification code". '
            'Current text does not match required format.'
        )
    
    return ValidationResult(True)

def validateTemplateName(name: str) -> ValidationResult:
    """
    Validate template name format.
    
    Args:
        name: Template name to validate
        
    Returns:
        ValidationResult with validation status and error message
    """
    nameRegex = re.compile(r'^[a-z0-9_]+$')
    
    if not nameRegex.match(name):
        return ValidationResult(
            False,
            'Template name must be lowercase letters, numbers, underscores only'
        )
    
    if len(name) > 512:
        return ValidationResult(
            False,
            'Template name exceeds 512 characters'
        )
    
    return ValidationResult(True)

def validateUrls(buttons: List[Dict[str, Any]]) -> ValidationResult:
    """
    Validate URL format and requirements.
    
    Args:
        buttons: List of button objects
        
    Returns:
        ValidationResult with validation status and error message
    """
    for button in buttons:
        if button.get('type') == 'URL' and button.get('url'):
            url = button['url']
            
            if not url.startswith('https://'):
                return ValidationResult(
                    False,
                    f'URL must use HTTPS: {url}'
                )
            
            if len(url) > 2000:
                return ValidationResult(
                    False,
                    f'URL exceeds 2000 character limit: {len(url)}'
                )
    
    return ValidationResult(True)

def validatePhoneNumbers(buttons: List[Dict[str, Any]]) -> ValidationResult:
    """
    Validate phone number format.
    
    Args:
        buttons: List of button objects
        
    Returns:
        ValidationResult with validation status and error message
    """
    phoneRegex = re.compile(r'^\+\d{10,15}$')
    
    for button in buttons:
        if button.get('type') == 'PHONE_NUMBER' and button.get('phone_number'):
            phone = button['phone_number']
            
            if not phoneRegex.match(phone):
                return ValidationResult(
                    False,
                    f'Phone number must be international format with +: {phone}'
                )
    
    return ValidationResult(True)

def validateMediaHeaders(header: Optional[Dict[str, Any]]) -> ValidationResult:
    """
    Validate media header format and requirements.
    
    Args:
        header: Header object to validate
        
    Returns:
        ValidationResult with validation status and error message
    """
    if not header or header.get('format') == 'TEXT':
        return ValidationResult(True)
    
    validFormats = {
        'IMAGE': ['.jpg', '.jpeg', '.png'],
        'VIDEO': ['.mp4'],
        'DOCUMENT': ['.pdf']
    }
    
    if header.get('format') and header.get('example', {}).get('header_url'):
        url = header['example']['header_url'][0]
        
        if not url.startswith('https://'):
            return ValidationResult(False, 'Media URLs must use HTTPS')
        
        validExtensions = validFormats.get(header['format'], [])
        hasValidExtension = any(url.lower().endswith(ext) for ext in validExtensions)
        
        if not hasValidExtension:
            return ValidationResult(
                False,
                f"{header['format']} header must end with: {', '.join(validExtensions)}"
            )
    
    return ValidationResult(True)

def validateComponentStructure(components: List[Dict[str, Any]]) -> ValidationResult:
    """
    Validate component structure requirements.
    
    Args:
        components: List of component objects
        
    Returns:
        ValidationResult with validation status and error message
    """
    # Check for required BODY component
    requiredBodyFound = any(c.get('type') == 'BODY' for c in components)
    if not requiredBodyFound:
        return ValidationResult(False, 'BODY component is required for all templates')
    
    # Check for duplicate components (except buttons)
    componentTypes = [c.get('type') for c in components]
    duplicates = [
        comp_type for comp_type in set(componentTypes)
        if componentTypes.count(comp_type) > 1 and comp_type != 'BUTTONS'
    ]
    
    if duplicates:
        return ValidationResult(
            False,
            f'Duplicate components not allowed: {", ".join(duplicates)}'
        )
    
    return ValidationResult(True)

def validateTemplateCategory(category: str) -> ValidationResult:
    """
    Validate template category.
    
    Args:
        category: Category to validate
        
    Returns:
        ValidationResult with validation status and error message
    """
    validCategories = ['MARKETING', 'UTILITY', 'AUTHENTICATION']
    
    if category.upper() not in validCategories:
        return ValidationResult(
            False,
            f'Invalid category: {category}. Must be one of: {", ".join(validCategories)}'
        )
    
    return ValidationResult(True)

def validateLanguageCode(language: str) -> ValidationResult:
    """
    Validate language code format.
    
    Args:
        language: Language code to validate
        
    Returns:
        ValidationResult with validation status and error message
    """
    languageRegex = re.compile(r'^[a-z]{2}_[A-Z]{2}$')
    
    if not languageRegex.match(language):
        return ValidationResult(
            False,
            f'Invalid language code format: {language}. Must be in format: en_US, es_ES, etc.'
        )
    
    return ValidationResult(True)

def validateCompleteTemplate(templateData: Dict[str, Any]) -> ValidationResult:
    """
    Comprehensive template validation combining all validation functions.
    
    Args:
        templateData: Complete template data dictionary
        
    Returns:
        ValidationResult with validation status and all error messages
    """
    errors = []
    
    # Extract template components
    name = templateData.get('name', '')
    category = templateData.get('category', '')
    language = templateData.get('language', '')
    components = templateData.get('components', [])
    
    # Basic validations
    nameValidation = validateTemplateName(name)
    if not nameValidation.isValid:
        errors.append(nameValidation.error)
    
    categoryValidation = validateTemplateCategory(category)
    if not categoryValidation.isValid:
        errors.append(categoryValidation.error)
    
    languageValidation = validateLanguageCode(language)
    if not languageValidation.isValid:
        errors.append(languageValidation.error)
    
    # Component structure validation
    structureValidation = validateComponentStructure(components)
    if not structureValidation.isValid:
        errors.append(structureValidation.error)
    
    # Extract all text for emoji validation
    allText = []
    allButtons = []
    
    for component in components:
        compType = component.get('type', '')
        
        if compType == 'BODY':
            text = component.get('text', '')
            allText.append(text)
            
            # Validate body character limit
            bodyValidation = validateCharacterLimits('body', text)
            if not bodyValidation.isValid:
                errors.append(bodyValidation.error)
            
            # Validate formatting
            formatValidation = validateFormatting(text)
            if not formatValidation.isValid and formatValidation.errors:
                errors.extend(formatValidation.errors)
        
        elif compType == 'HEADER':
            if component.get('format') == 'TEXT':
                text = component.get('text', '')
                allText.append(text)
                
                # Validate header character limit
                headerValidation = validateCharacterLimits('header', text)
                if not headerValidation.isValid:
                    errors.append(headerValidation.error)
                
                # Validate formatting
                formatValidation = validateFormatting(text)
                if not formatValidation.isValid and formatValidation.errors:
                    errors.extend(formatValidation.errors)
            
            # Validate media header
            mediaValidation = validateMediaHeaders(component)
            if not mediaValidation.isValid:
                errors.append(mediaValidation.error)
        
        elif compType == 'FOOTER':
            text = component.get('text', '')
            allText.append(text)
            
            # Validate footer character limit
            footerValidation = validateCharacterLimits('footer', text)
            if not footerValidation.isValid:
                errors.append(footerValidation.error)
            
            # Validate formatting
            formatValidation = validateFormatting(text)
            if not formatValidation.isValid and formatValidation.errors:
                errors.extend(formatValidation.errors)
        
        elif compType == 'BUTTONS':
            buttons = component.get('buttons', [])
            allButtons.extend(buttons)
            
            # Validate button text
            buttonTextValidation = validateButtonText(buttons)
            if not buttonTextValidation.isValid:
                errors.append(buttonTextValidation.error)
            
            # Validate URLs
            urlValidation = validateUrls(buttons)
            if not urlValidation.isValid:
                errors.append(urlValidation.error)
            
            # Validate phone numbers
            phoneValidation = validatePhoneNumbers(buttons)
            if not phoneValidation.isValid:
                errors.append(phoneValidation.error)
            
            # Validate button combinations
            buttonComboValidation = validateButtonCombinations('TEMPLATE', buttons)
            if not buttonComboValidation.isValid:
                errors.append(buttonComboValidation.error)
    
    # Validate emoji limit across all text
    emojiValidation = validateEmojiLimit(allText)
    if not emojiValidation.isValid:
        errors.append(emojiValidation.error)
    
    # Validate authentication format if applicable
    if category.upper() == 'AUTHENTICATION':
        bodyText = next((c.get('text', '') for c in components if c.get('type') == 'BODY'), '')
        authValidation = validateAuthenticationFormat(bodyText)
        if not authValidation.isValid:
            errors.append(authValidation.error)
    
    return ValidationResult(len(errors) == 0, errors=errors if errors else None)

def formatValidationErrors(validationResult: ValidationResult) -> Dict[str, Any]:
    """
    Format validation errors for API response.
    
    Args:
        validationResult: Validation result object
        
    Returns:
        Formatted error response dictionary
    """
    if validationResult.isValid:
        return {"success": True}
    
    if validationResult.errors:
        return {
            "success": False,
            "validation_errors": [
                {
                    "field": "template",
                    "message": error
                }
                for error in validationResult.errors
            ]
        }
    
    return {
        "success": False,
        "validation_errors": [
            {
                "field": "template",
                "message": validationResult.error
            }
        ]
    }
