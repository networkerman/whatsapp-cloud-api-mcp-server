# WhatsApp Cloud API Comprehensive MCP Server

This is a comprehensive MCP (Model Context Protocol) server that provides full access to the WhatsApp Cloud API capabilities, including messaging, templates, business management, media handling, and more.

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

## Requirements

- Python 3.12 or higher
- uv (Python package manager)
- Meta WhatsApp Business API credentials

## Installation

1. Clone the repository:
```bash
git clone https://github.com/deuslirio/mcp-server-whatsapp-message.git
cd mcp-server-whatsapp-message
```

2. Install dependencies using uv:
```bash
uv pip install -e .
```

## Environment Variables

Set up your WhatsApp Business API credentials:

```bash
# Required for all operations
META_ACCESS_TOKEN=your_access_token_here
META_PHONE_NUMBER_ID=your_phone_number_id_here

# Required for templates and business operations  
META_BUSINESS_ACCOUNT_ID=your_business_account_id_here

# Optional - API version (defaults to v22.0)
WHATSAPP_API_VERSION=v22.0
```

## Running the Server

### Standalone Mode
```bash
uv run python main.py
```

### Integration with Claude Local
Add to your Claude configuration:

```json
{
    "mcpServers": {
        "whatsapp": {
            "command": "uv",
            "args": ["run", "python", "main.py"],
            "cwd": "/path/to/mcp-server-whatsapp-message",
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

## Demo

Here are some screenshots demonstrating the WhatsApp Message Sender MCP Tool in action:

### Sending a Message
![Sending a WhatsApp message](https://github.com/user-attachments/assets/58fc3c58-b584-4d7f-9646-c4eb23c2af81)

### Receiving a Message
![Receiving a WhatsApp message](https://github.com/user-attachments/assets/c9e6a5d3-e488-4900-a222-6fff1e403f28)

### Using the Contacts Resource
![Accessing the contacts resource](https://github.com/user-attachments/assets/dd13c180-d286-4284-bb9c-f086b321f1b4)

### Received Message
![Received Message](https://github.com/user-attachments/assets/d5862915-1787-4c95-81c1-8eca7388bdc3)

## Troubleshooting

### Common Issues

1. **FastMCP Import Error**:
   - Verify that the `mcp` package is installed correctly:
     ```bash
     uv pip install mcp==1.6.0
     ```

2. **Environment Variables Error**:
   - Make sure the environment variables are correctly set in your Claude Local configuration
   - Verify that the variable values are correct

3. **Error when running with uv run**:
   - Try clearing the uv cache:
     ```bash
     uv cache clean
     ```
   - Reinstall dependencies:
     ```bash
     uv pip install -e .
     ```

## Project Structure

```
mcp-server-whatsapp-message/
├── main.py                  # Server entry point
├── mcp_server/              # Main module
│   ├── __init__.py          # Module initialization
│   └── whatsapp_handler.py  # WhatsApp message handler
├── pyproject.toml           # Project configuration
├── requirements.txt         # Project dependencies
└── .env                     # Environment variables (not versioned)
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
