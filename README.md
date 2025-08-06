# WhatsApp Cloud API Comprehensive MCP Server

This is a comprehensive MCP (Model Context Protocol) server that provides full access to the WhatsApp Cloud API capabilities, including messaging, templates, business management, media handling, and more.

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

## 🚀 Quick Start Installation

> **Important:** This is a comprehensive WhatsApp Cloud API MCP server that requires proper setup to function correctly.

### Prerequisites

- **Python 3.12 or higher** - Required for modern async support
- **uv (Python package manager)** - Fast Python package installer
- **Meta WhatsApp Business API credentials** - Get these from [Meta Business](https://business.facebook.com/)

### Step-by-Step Installation

1. **Install dependencies:**
   ```bash
   uv pip install -e .
   ```

2. **Verify installation:**
   ```bash
   uv run python -c "import mcp_server; print('Installation successful!')"
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
            "cwd": "/path/to/whatsapp-cloud-api-mcp-server",
            "env": {
                "META_ACCESS_TOKEN": "your-token-here",
                "META_PHONE_NUMBER_ID": "your-phone-id-here",
                "META_BUSINESS_ACCOUNT_ID": "your-business-account-id-here"
            }
        }
    }
}
```

## 🌐 Remote Deployment Options

### Option 1: HTTP REST API Server (Recommended for Public Access)

Deploy as a traditional HTTP REST API that can be accessed from anywhere:

```bash
# Run locally
python server_http.py

# Or use the deployment script
./deploy.sh
```

**Features:**
- 🌐 Standard HTTP REST API (Port 8080)
- 📚 Auto-generated API documentation at `/docs`
- 🔍 Health checks at `/health`
- 🧭 CORS enabled for web clients
- 📱 All WhatsApp operations via HTTP endpoints

**API Endpoints:**
- `POST /api/v1/messaging/send-text` - Send text messages
- `POST /api/v1/messaging/send-image` - Send images
- `POST /api/v1/templates/send` - Send template messages
- `GET /api/v1/templates/` - List templates
- `GET /api/v1/business/profile` - Get business profile

### Option 2: SSE MCP Server

Deploy with Server-Sent Events for MCP protocol compatibility:

```bash
# Run locally
python server_sse.py

# Access via SSE endpoint
# http://localhost:8000/sse
```

**Features:**
- 📡 Native MCP protocol support (Port 8000)
- 🔄 Real-time bidirectional communication
- 🛠️ Full tool and resource support
- 🔌 Compatible with MCP clients

### 🐳 Docker Deployment

#### Quick Start with Docker
```bash
# Copy environment template
cp .env.example .env
# Edit .env with your WhatsApp credentials

# HTTP Server
docker build -t whatsapp-mcp .
docker run -p 8080:8080 --env-file .env whatsapp-mcp python server_http.py

# SSE Server
docker run -p 8000:8000 --env-file .env whatsapp-mcp python server_sse.py
```

#### Docker Compose (Production Ready)
```bash
# HTTP Server only
docker-compose up whatsapp-mcp-http

# SSE Server only
docker-compose --profile sse up whatsapp-mcp-sse

# Both servers
docker-compose --profile sse up
```

### ☁️ Cloud Deployment

#### Railway (Recommended)
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically

#### Heroku
1. Create `Procfile`: `web: python server_http.py`
2. Set Config Vars with environment variables
3. Deploy via Git

#### Digital Ocean App Platform
1. Connect GitHub repository
2. Configure environment variables
3. Auto-deploy on push

#### VPS Deployment
```bash
# On your VPS
git clone https://github.com/your-username/whatsapp-cloud-api-mcp-server.git
cd whatsapp-cloud-api-mcp-server
cp .env.example .env
# Edit .env with your credentials
docker-compose up -d
```

### 🔧 Environment Variables for Deployment

```bash
# Required
META_ACCESS_TOKEN=your_meta_access_token
META_PHONE_NUMBER_ID=your_phone_number_id
META_BUSINESS_ACCOUNT_ID=your_business_account_id

# Server Config
HTTP_SERVER_HOST=0.0.0.0  # For public access
HTTP_SERVER_PORT=8080
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
```

### 🚀 Quick Deployment Script

Use the included deployment script for easy setup:

```bash
./deploy.sh
```

This interactive script guides you through:
- Environment validation
- Server mode selection (HTTP/SSE)
- Docker deployment options
- Cloud deployment guidance

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
whatsapp-cloud-api-mcp-server/
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
