# 🚀 Deploy SSE MCP Server to Railway for ElevenLabs

This guide helps you deploy a separate SSE MCP server for ElevenLabs integration.

## 🎯 **Why SSE Server?**

- **HTTP Server**: For general API access, Claude website, curl commands
- **SSE Server**: For MCP integrations (ElevenLabs, Claude Desktop, etc.)

## 📋 **Step-by-Step Railway Deployment**

### **Step 1: Create New Railway Service**

1. **Go to Railway Dashboard**: [railway.app](https://railway.app)
2. **Open your existing project** (where your HTTP server is)
3. **Click "New Service"** (don't create a new project)
4. **Select "GitHub Repo"**
5. **Choose your repository**: `networkerman/whatsapp-cloud-api-mcp-server`

### **Step 2: Configure the SSE Service**

#### **A. Set Start Command**
In Railway service settings:
```
python server_sse.py
```

#### **B. Set Environment Variables**
Add these **exact** variables:

```
META_ACCESS_TOKEN=EAAMexKBZAbb0BO2SCgi092ScWMfsKrcsAaKnJhBnjX0ZCWxCVn6qWquoSjvaHNrttGgmJIFdffxLnwn8qlcJbPh8ZCjsfZAmGXfZAWal9GRy9w5gImztuDUmdRRumOvrJ7OfXzMxHUpUpUkZBiTYDzHFikMPi58sKGzZCKm5HMwFkQRzOlE4JXwGxsg6eugAQgz

META_PHONE_NUMBER_ID=2395491917210830

META_BUSINESS_ACCOUNT_ID=your_meta_business_account_id

WABA_ID=354081058707811

WHATSAPP_API_VERSION=v22.0

MCP_SERVER_HOST=0.0.0.0

MCP_SERVER_PORT=8000
```

#### **C. Set Port**
- **Port**: `8000`

### **Step 3: Deploy**
1. **Click "Deploy"**
2. **Wait for build and deployment**
3. **Get your SSE service URL** (something like): 
   ```
   https://whatsapp-sse-server-production.up.railway.app
   ```

## 🔗 **ElevenLabs Configuration**

### **Once your SSE server is deployed:**

**Server Type**: `SSE`  
**Server URL**: `https://your-sse-service-url.railway.app`  
**HTTP Headers**: Leave empty  

### **Example URLs:**
- **SSE Endpoint**: `https://your-sse-service-url.railway.app/sse`
- **Health Check**: `https://your-sse-service-url.railway.app/health`

## ✅ **Verification Steps**

### **1. Check SSE Server Health**
Visit in browser:
```
https://your-sse-service-url.railway.app/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "WhatsApp MCP SSE Server"
}
```

### **2. Check SSE Endpoint**
The SSE endpoint should be:
```
https://your-sse-service-url.railway.app/sse
```

### **3. Test in ElevenLabs**
- Add the SSE URL to ElevenLabs
- Test a simple MCP call
- Verify WhatsApp message sending works

## 📊 **Project Structure After Deployment**

You'll have **TWO Railway services**:

1. **HTTP Server** (`whatsapp-cloud-api-mcp-server-production`):
   - Port 8080
   - REST API for general use
   - `/docs` endpoint for testing

2. **SSE Server** (`whatsapp-sse-server-production`):
   - Port 8000
   - MCP protocol for integrations
   - `/sse` endpoint for MCP clients

## 🔧 **Troubleshooting**

### **If SSE Server Won't Start:**
1. Check Railway logs for errors
2. Verify all environment variables are set
3. Ensure start command is `python server_sse.py`

### **If ElevenLabs Can't Connect:**
1. Use the public Railway URL (not `.railway.internal`)
2. Ensure port 8000 is exposed
3. Test the `/sse` endpoint directly

### **If WhatsApp Functions Don't Work:**
1. Check environment variables match your working HTTP server
2. Verify both `META_BUSINESS_ACCOUNT_ID` and `WABA_ID` are set
3. Test with a simple text message first

## 🎉 **You're Done!**

Your SSE MCP server is now ready for ElevenLabs integration! The SSE server provides the same WhatsApp functionality as your HTTP server but uses the MCP protocol that ElevenLabs expects.

**Both servers can run simultaneously and serve different purposes:**
- **HTTP**: For general API access, testing, Claude website
- **SSE**: For MCP integrations like ElevenLabs, Claude Desktop