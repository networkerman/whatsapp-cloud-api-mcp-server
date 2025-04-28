from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from mcp_server import WhatsAppHandler, WhatsAppMessage
from typing import List, Dict

# Load environment variables
load_dotenv()

# Initialize the WhatsApp handler
whatsapp_handler = WhatsAppHandler()

# Create FastMCP app
mcp = FastMCP(title="WhatsApp Message Sender")

# Define contacts resource
contacts = [
    {"name": "João da Silva", "phone_number": "+55629999999999"},
]

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

@mcp.resource("resource://contacts")
async def get_contacts() -> List[Dict[str, str]]:
    """
    Get a list of contacts with their names and phone numbers.
    
    Returns:
        List[Dict[str, str]]: A list of contacts with name and phone_number
    """
    return contacts

# @mcp.tool()
# async def send_message_to_contact(contact_name: str, message: str) -> dict:
#     """
#     Send a WhatsApp message to a contact by name.
    
#     Args:
#         contact_name: The name of the contact to send the message to
#         message: The message to send
        
#     Returns:
#         dict: Response containing status and message details
#     """
#     # Find the contact by name
#     contact = next((c for c in contacts if c["name"].lower() == contact_name.lower()), None)
    
#     if not contact:
#         raise ValueError(f"Contact '{contact_name}' not found")
    
#     # Send the message
#     return await send_whatsapp_message(contact["phone_number"], message)


if __name__ == "__main__":
    # Para executar com uv run, use: uv run python main.py
    mcp.run(transport='stdio')