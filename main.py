from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from mcp_server import WhatsAppHandler, WhatsAppMessage

# Load environment variables
load_dotenv()

# Initialize the WhatsApp handler
whatsapp_handler = WhatsAppHandler()

# Create FastMCP app
mcp = FastMCP(title="WhatsApp Message Sender")

@mcp.tool()
async def send_whatsapp_message(phone_number: str, message: str) -> dict:
    """
    Send a WhatsApp message to a specified phone number.
    
    Args:
        phone_number: The recipient's phone number (with country code, e.g., +5511999999999)
        message: The message to send
        
    Returns:
        dict: Response containing status and message details
    """
    message_data = WhatsAppMessage(
        phone_number=phone_number,
        message=message
    )
    
    if not whatsapp_handler.validate_message(message_data):
        raise ValueError("Invalid message data")
        
    result = await whatsapp_handler.send_message(message_data)
    return result


if __name__ == "__main__":
    # Para executar com uv run, use: uv run python main.py
    mcp.run(transport='stdio')