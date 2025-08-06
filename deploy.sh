#!/bin/bash

# WhatsApp Cloud API MCP Server Deployment Script
# This script helps deploy the server in different modes

set -e

echo "🚀 WhatsApp Cloud API MCP Server Deployment"
echo "=============================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "📋 Please copy .env.example to .env and configure your settings:"
    echo "   cp .env.example .env"
    echo "   # Edit .env with your WhatsApp API credentials"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Validate required environment variables
required_vars=("META_ACCESS_TOKEN" "META_PHONE_NUMBER_ID")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "❌ Missing required environment variables:"
    printf "   %s\n" "${missing_vars[@]}"
    echo "📝 Please configure these in your .env file"
    exit 1
fi

echo "✅ Environment variables validated"

# Function to display menu
show_menu() {
    echo ""
    echo "Select deployment mode:"
    echo "1) HTTP REST API Server (Port 8080)"
    echo "2) SSE MCP Server (Port 8000)"
    echo "3) Docker HTTP Server"
    echo "4) Docker SSE Server"
    echo "5) Docker Compose (Both servers)"
    echo "6) Cloud Deployment Guide"
    echo "7) Exit"
    echo ""
}

# Function to run HTTP server
run_http_server() {
    echo "🌐 Starting HTTP REST API Server..."
    echo "📡 Will be available at: http://localhost:8080"
    echo "📚 API Documentation: http://localhost:8080/docs"
    echo ""
    python server_http.py
}

# Function to run SSE server
run_sse_server() {
    echo "📡 Starting SSE MCP Server..."
    echo "🔗 Will be available at: http://localhost:8000"
    echo "🔌 SSE Endpoint: http://localhost:8000/sse"
    echo ""
    python server_sse.py
}

# Function to run Docker HTTP
run_docker_http() {
    echo "🐳 Building and starting Docker HTTP server..."
    docker build -t whatsapp-mcp-server .
    docker run -p 8080:8080 --env-file .env whatsapp-mcp-server python server_http.py
}

# Function to run Docker SSE
run_docker_sse() {
    echo "🐳 Building and starting Docker SSE server..."
    docker build -t whatsapp-mcp-server .
    docker run -p 8000:8000 --env-file .env whatsapp-mcp-server python server_sse.py
}

# Function to run Docker Compose
run_docker_compose() {
    echo "🐳 Starting with Docker Compose..."
    echo "📖 Choose which server to start:"
    echo "1) HTTP Server only"
    echo "2) SSE Server only"
    echo "3) Both servers"
    read -p "Enter your choice (1-3): " compose_choice
    
    case $compose_choice in
        1)
            docker-compose up --build whatsapp-mcp-http
            ;;
        2)
            docker-compose --profile sse up --build whatsapp-mcp-sse
            ;;
        3)
            docker-compose --profile sse up --build
            ;;
        *)
            echo "❌ Invalid choice"
            ;;
    esac
}

# Function to show cloud deployment guide
show_cloud_guide() {
    echo ""
    echo "☁️  CLOUD DEPLOYMENT GUIDE"
    echo "=========================="
    echo ""
    echo "🚀 For production deployment, you can use:"
    echo ""
    echo "1️⃣  RAILWAY (Recommended)"
    echo "   • Connect your GitHub repository"
    echo "   • Set environment variables in Railway dashboard"
    echo "   • Deploy command: python server_http.py"
    echo "   • Railway will auto-assign a public URL"
    echo ""
    echo "2️⃣  HEROKU"
    echo "   • Create Procfile: web: python server_http.py"
    echo "   • Set Config Vars with your environment variables"
    echo "   • Deploy via Git or GitHub integration"
    echo ""
    echo "3️⃣  DIGITAL OCEAN APP PLATFORM"
    echo "   • Connect GitHub repository"
    echo "   • Configure environment variables"
    echo "   • Use HTTP server mode for web apps"
    echo ""
    echo "4️⃣  AWS ECS / GOOGLE CLOUD RUN"
    echo "   • Use the provided Dockerfile"
    echo "   • Configure environment variables in the cloud console"
    echo "   • Scale as needed"
    echo ""
    echo "5️⃣  VPS DEPLOYMENT"
    echo "   • Copy files to your VPS"
    echo "   • Install Docker and use: docker-compose up -d"
    echo "   • Configure reverse proxy (nginx) for HTTPS"
    echo ""
    echo "📋 Required Environment Variables for all platforms:"
    echo "   • META_ACCESS_TOKEN"
    echo "   • META_PHONE_NUMBER_ID"
    echo "   • META_BUSINESS_ACCOUNT_ID"
    echo ""
    read -p "Press Enter to continue..."
}

# Main menu loop
while true; do
    show_menu
    read -p "Enter your choice (1-7): " choice
    
    case $choice in
        1)
            run_http_server
            ;;
        2)
            run_sse_server
            ;;
        3)
            run_docker_http
            ;;
        4)
            run_docker_sse
            ;;
        5)
            run_docker_compose
            ;;
        6)
            show_cloud_guide
            ;;
        7)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please select 1-7."
            ;;
    esac
done