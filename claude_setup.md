# 🔗 Connecting Your WhatsApp Server to Claude

## 📋 **Quick Setup Guide**

### **Method 1: Using the MCP Client (Recommended)**

1. **Add to Claude Desktop configuration:**

```json
{
  "mcpServers": {
    "whatsapp-cloud-api": {
      "command": "uv",
      "args": ["run", "python", "claude_client.py"],
      "cwd": "/Users/ud/whatsapp-cloud-api-mcp-server"
    }
  }
}
```

2. **Restart Claude Desktop**

3. **Test in Claude:**
   ```
   Please send a WhatsApp message to +919823329163 saying "Hello from Claude!"
   ```

### **Method 2: Direct HTTP Connection**

```json
{
  "mcpServers": {
    "whatsapp-api": {
      "command": "npx",
      "args": [
        "-y", 
        "@modelcontextprotocol/server-fetch",
        "https://whatsapp-cloud-api-mcp-server-production.up.railway.app"
      ]
    }
  }
}
```

## 🎯 **Available Claude Commands**

Once connected, you can ask Claude to:

### **📱 Send Messages:**
```
"Send a WhatsApp message to +919823329163 saying 'Meeting at 3 PM today'"
```

### **📋 Send Templates:**
```
"Send a hello_world template to +919823329163"
```

### **📊 Get Information:**
```
"Show me my WhatsApp business profile"
"List all available WhatsApp templates"
```

### **🔍 Check Status:**
```
"Check the status of my WhatsApp server"
```

## 🛠️ **Configuration File Locations**

### **macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

### **Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### **Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

## 🧪 **Testing Your Connection**

1. **Open Claude Desktop**
2. **Ask:** "Can you check my WhatsApp server status?"
3. **Ask:** "Send a test message to +919823329163"
4. **Ask:** "Show me my available WhatsApp templates"

## 🔧 **Troubleshooting**

### **If MCP Client Doesn't Work:**
1. Check your `claude_desktop_config.json` syntax
2. Ensure the path to your project is correct
3. Restart Claude Desktop completely
4. Check Claude's logs for errors

### **If Railway Server is Down:**
- Check your Railway deployment logs
- Verify environment variables are set
- Test the server directly: https://whatsapp-cloud-api-mcp-server-production.up.railway.app/health

### **Common Issues:**
- **Path errors:** Use absolute paths in the configuration
- **Permission errors:** Ensure Claude can access the project directory
- **Network errors:** Check if Railway URL is accessible

## 🎉 **You're All Set!**

Your WhatsApp server is now connected to Claude! You can send messages, manage templates, and get business information directly through Claude conversations.

**Example conversation:**
```
User: "Send a WhatsApp message to my number saying hello"
Claude: I'll send that WhatsApp message for you!
[Calls send_whatsapp_text tool]
Message sent successfully to +919823329163!
```