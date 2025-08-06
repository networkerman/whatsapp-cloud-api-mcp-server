# MCP Inspector Setup Guide

## 🧪 **Testing Your WhatsApp MCP Server with MCP Inspector**

The MCP Inspector is a powerful tool for testing and debugging MCP servers. Here's how to use it with your WhatsApp MCP server.

## 📋 **Prerequisites**

1. **Node.js installed** (for npx)
2. **Your MCP server running locally**
3. **Environment variables set**

## 🚀 **Quick Start**

### **Step 1: Start Your MCP Server**

```bash
# In your project directory
cd /Users/ud/whatsapp-cloud-api-mcp-server
source venv/bin/activate

# Set environment variables
export META_ACCESS_TOKEN="your_access_token"
export META_PHONE_NUMBER_ID="your_phone_number_id"
export WABA_ID="your_waba_id"
export META_BUSINESS_ACCOUNT_ID="your_business_account_id"

# Start the server
python main.py
```

### **Step 2: Launch MCP Inspector**

In a **new terminal window**:

```bash
# For Python servers (your case)
npx @modelcontextprotocol/inspector \
  uv \
  --directory /Users/ud/whatsapp-cloud-api-mcp-server \
  run \
  whatsapp-cloud-api-mcp-server
```

**Alternative method (if uv doesn't work):**

```bash
npx @modelcontextprotocol/inspector \
  python \
  /Users/ud/whatsapp-cloud-api-mcp-server/main.py
```

## 🔧 **Inspector Features**

### **Server Connection Pane**
- **Transport**: Select `stdio` (default for local servers)
- **Command**: Verify the command points to your `main.py`
- **Environment**: Add your environment variables

### **Tools Tab**
Test your WhatsApp tools:
- `send_whatsapp_message`
- `send_template_message`
- `get_business_profile`
- `get_message_templates`
- `get_phone_numbers`
- `upload_media`
- `download_media`

### **Resources Tab**
- View available resources
- Test resource subscriptions

### **Notifications Pane**
- Monitor server logs
- View real-time notifications

## 🧪 **Testing Examples**

### **Test Business Profile**
1. Go to **Tools** tab
2. Find `get_business_profile`
3. Click **Test**
4. View the response

### **Test Template List**
1. Go to **Tools** tab
2. Find `get_message_templates`
3. Click **Test**
4. Browse your templates

### **Test Message Sending**
1. Go to **Tools** tab
2. Find `send_whatsapp_message`
3. Click **Test**
4. Enter parameters:
   ```json
   {
     "phone_number": "+919823329163",
     "message": "Hello from MCP Inspector!"
   }
   ```

## 🔍 **Debugging Tips**

### **Common Issues**

1. **Server not starting**
   - Check environment variables
   - Verify Python dependencies
   - Check port conflicts

2. **Tools not appearing**
   - Ensure server is running
   - Check capability negotiation
   - Verify tool registration

3. **Connection errors**
   - Check transport settings
   - Verify command path
   - Check permissions

### **Development Workflow**

1. **Start Development**
   ```bash
   # Terminal 1: Start server
   python main.py
   
   # Terminal 2: Start inspector
   npx @modelcontextprotocol/inspector python main.py
   ```

2. **Iterative Testing**
   - Make changes to your server
   - Restart the server
   - Reconnect inspector
   - Test affected features

3. **Edge Case Testing**
   - Test invalid inputs
   - Test missing parameters
   - Verify error handling

## 📚 **Additional Resources**

- [MCP Inspector Repository](https://github.com/modelcontextprotocol/inspector)
- [MCP Debugging Guide](https://modelcontextprotocol.io/legacy/tools/debugging)
- [MCP Documentation](https://modelcontextprotocol.io/)

## 🎯 **Next Steps**

1. **Test all your tools** in the Inspector
2. **Verify error handling** with invalid inputs
3. **Test concurrent operations**
4. **Monitor performance** and logs
5. **Document any issues** you find

---

**Happy Testing! 🚀** 