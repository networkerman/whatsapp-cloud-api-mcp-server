# WhatsApp Cloud API MCP Server

A clean, simple MCP (Model Context Protocol) server that provides comprehensive access to the WhatsApp Cloud API capabilities, including messaging, templates, business management, and media handling.

## Author

**Udayan Das Chowdhury**  
Lead Product Manager driving Omnichannel Product Management at Netcore Cloud  
LinkedIn: [@udayan-das-chowdhury8329](https://www.linkedin.com/in/udayan-das-chowdhury8329/)

## Features

### 🚀 **Complete WhatsApp Cloud API Coverage**
- **Text Messaging** - Send text messages with URL previews and replies
- **Media Messaging** - Send images, videos, audio, documents, and stickers
- **Interactive Messages** - Send buttons and list messages
- **Location & Contacts** - Send location pins and contact cards
- **Message Reactions** - React to messages with emojis
- **Template Management** - Create, manage, and send template messages
- **Business Profile** - Manage business profile information
- **Phone Number Management** - Register and verify phone numbers
- **Media Upload** - Upload and manage media files
- **Message Status** - Mark messages as read and track delivery

### 📱 **Based on Official API**
Built from the official [WhatsApp Cloud API Postman collection](https://www.postman.com/meta/whatsapp-business-platform/collection/wlk6lh4/whatsapp-cloud-api), ensuring 100% API compatibility and coverage.

## 🚀 Quick Start

### Prerequisites

- **Python 3.10 or higher** - Required for MCP support
- **Meta WhatsApp Business API credentials** - Get these from [Meta Business](https://business.facebook.com/)

### Step-by-Step Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd whatsapp-cloud-api-mcp-server
   ```

2. **Set up environment variables:**
   ```bash
   # Run the setup script to create .env file
   python setup.py
   
   # Then edit .env file with your actual credentials
   # Or set environment variables directly:
   export META_ACCESS_TOKEN=your_access_token_here
   export META_PHONE_NUMBER_ID=your_phone_number_id_here
   ```

3. **Install dependencies:**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python diagnose.py
   ```

### Troubleshooting Connection Issues

If you're getting "Server disconnected" errors when connecting to Claude, run the diagnostic script:

```bash
python diagnose.py
```

This will check your setup and identify common issues like:

1. **Python version incompatibility** - MCP requires Python 3.10+
2. **Missing environment variables** - Required WhatsApp API credentials
3. **Missing dependencies** - Required Python packages
4. **Configuration errors** - Invalid API credentials

**Quick fixes:**

```bash
# 1. Check your setup
python diagnose.py

# 2. If Python version is wrong (3.9.x), upgrade:
brew install python@3.12

# 3. If missing .env file:
python setup.py

# 4. If missing dependencies:
pip install mcp httpx python-dotenv

# 5. Run diagnostic again
python diagnose.py
```

For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Environment Variables

Set up your WhatsApp Business API credentials:

```bash
# Required for all operations
META_ACCESS_TOKEN=your_access_token_here
META_PHONE_NUMBER_ID=your_phone_number_id_here

# Business Account IDs (recommended to set both for maximum compatibility)
META_BUSINESS_ACCOUNT_ID=your_meta_business_account_id_here  # For templates and business operations
WABA_ID=your_waba_id_here                                    # For phone numbers and WABA operations

# Optional - API version (defaults to v22.0)
WHATSAPP_API_VERSION=v22.0
```

## Running the Server

### Standalone Mode
```bash
python main.py
```

### Integration with Claude Desktop
Add to your Claude configuration:

```json
{
    "mcpServers": {
        "whatsapp": {
            "command": "/path/to/your/project/venv/bin/python",
            "args": ["main.py"],
            "cwd": "/path/to/your/project",
            "env": {
                "META_ACCESS_TOKEN": "your-token-here",
                "META_PHONE_NUMBER_ID": "your-phone-id-here",
                "META_BUSINESS_ACCOUNT_ID": "your-business-account-id-here"
            }
        }
    }
}
```

## Available Tools

### 📝 **Text Messaging**
- `send_whatsapp_message` - Basic text message (legacy compatibility)
- `send_text_message` - Advanced text message with URL previews and replies
- `send_reaction` - React to messages with emojis

### 🖼️ **Media Messaging**
- `send_image_message` - Send images with captions
- `send_video_message` - Send videos with captions
- `send_audio_message` - Send audio files
- `send_document_message` - Send documents with filenames
- `send_sticker_message` - Send sticker messages

### 🎯 **Interactive Messaging**
- `send_button_message` - Send messages with interactive buttons
- `send_list_message` - Send messages with selectable lists

### 📍 **Location & Contacts**
- `send_location_message` - Send location pins with names and addresses
- `send_contact_message` - Send contact cards

### 📋 **Template Management**
- `get_message_templates` - List all templates with filtering
- `create_message_template` - Create new template messages
- `delete_message_template` - Delete existing templates
- `send_template_message` - Send template messages with parameters
- `send_template_with_media_header` - Send templates with media headers

### 📁 **Media Management**
- `upload_media` - Upload media files and get media IDs
- `get_media_info` - Get information about uploaded media
- `delete_media` - Delete uploaded media files

### 🏢 **Business Management**
- `get_business_profile` - Get business profile information
- `update_business_profile` - Update business profile details
- `get_phone_numbers` - List all business phone numbers
- `get_phone_number_info` - Get detailed phone number information
- `register_phone_number` - Register phone numbers with 2FA
- `verify_phone_number` - Verify phone numbers with codes

### ⚙️ **Utility Functions**
- `mark_message_as_read` - Mark received messages as read

## Available Resources

### 📚 **Dynamic Resources**
- `resource://contacts` - Sample contact list
- `resource://templates` - Live template data from your account
- `resource://business_profile` - Current business profile information

## Usage Examples

### Send a Text Message
```python
await send_text_message(
    phone_number="+1234567890",
    message="Hello from WhatsApp Cloud API!",
    preview_url=True
)
```

### Send a Template Message
```python
await send_template_message(
    phone_number="+1234567890", 
    template_name="hello_world",
    language_code="en_US",
    body_parameters=["John", "Welcome!"]
)
```

### Send an Interactive Button Message
```python
await send_button_message(
    phone_number="+1234567890",
    body_text="Choose an option:",
    buttons=[
        {"title": "Option 1", "id": "opt1"},
        {"title": "Option 2", "id": "opt2"}
    ],
    header_text="Please select"
)
```

### Upload and Send Media
```python
# Upload media
media_result = await upload_media(
    file_path="/path/to/image.jpg",
    media_type="image"
)

# Send media message
await send_image_message(
    phone_number="+1234567890",
    image_id=media_result["data"]["id"],
    caption="Check out this image!"
)
```

### Create a Template
```python
await create_message_template(
    name="welcome_template",
    category="UTILITY",
    language="en_US", 
    body_text="Welcome {{1}}! Your order {{2}} is confirmed.",
    header_text="Order Confirmation",
    footer_text="Thank you for your business"
)
```

## Project Structure

```
whatsapp-cloud-api-mcp-server/
├── main.py                  # Server entry point
├── comprehensive_tools.py   # All tool definitions
├── mcp_server/              # Core modules
│   ├── __init__.py          # Module initialization
│   ├── base_handler.py      # Base WhatsApp handler
│   ├── messaging_handler.py # Messaging operations
│   ├── template_handler.py  # Template operations
│   ├── business_handler.py  # Business operations
│   ├── media_handler.py     # Media operations
│   └── models.py            # Data models
├── setup.py                 # Setup script
├── diagnose.py              # Diagnostic script
├── requirements.txt         # Project dependencies
├── pyproject.toml           # Project configuration
└── .env                     # Environment variables (not versioned)
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.
