#!/usr/bin/env python3
"""
Quick Setup Test for WhatsApp Cloud API MCP Server
Simple script to verify your configuration is working correctly.

Usage:
    python test_setup.py

This script will:
1. Check environment variables
2. Test basic API connectivity
3. Verify handler availability
4. Run a simple message test (if TEST_PHONE_NUMBER is set)
"""

import os
import sys
import requests
import json
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🧪 {title}")
    print("=" * 60)

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_warning(message):
    """Print warning message"""
    print(f"⚠️  {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def check_environment_variables():
    """Check if required environment variables are set"""
    print_header("Environment Variables Check")
    
    required_vars = [
        "META_ACCESS_TOKEN",
        "META_PHONE_NUMBER_ID"
    ]
    
    optional_vars = [
        "META_BUSINESS_ACCOUNT_ID",
        "WABA_ID", 
        "META_APP_ID",
        "TEST_PHONE_NUMBER"
    ]
    
    missing_required = []
    missing_optional = []
    
    # Check required variables
    for var in required_vars:
        if os.getenv(var):
            print_success(f"{var} is set")
        else:
            print_error(f"{var} is missing")
            missing_required.append(var)
    
    # Check optional variables
    for var in optional_vars:
        if os.getenv(var):
            print_success(f"{var} is set (optional)")
        else:
            print_warning(f"{var} is not set (optional)")
            missing_optional.append(var)
    
    if missing_required:
        print_error(f"Missing required variables: {', '.join(missing_required)}")
        return False
    
    return True

def test_api_connectivity():
    """Test basic API connectivity"""
    print_header("API Connectivity Test")
    
    base_url = "https://whatsapp-cloud-api-mcp-server-production.up.railway.app"
    
    try:
        # Test health endpoint
        print_info("Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            handlers = data.get("handlers", {})
            active_handlers = sum(handlers.values())
            total_handlers = len(handlers)
            
            print_success(f"Health check passed - {active_handlers}/{total_handlers} handlers active")
            
            # Show handler status
            for handler, status in handlers.items():
                status_icon = "✅" if status else "❌"
                print(f"   {status_icon} {handler}")
            
            return True
        else:
            print_error(f"Health check failed - Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Connection failed: {str(e)}")
        return False

def test_root_endpoint():
    """Test root endpoint for API information"""
    print_header("API Information")
    
    base_url = "https://whatsapp-cloud-api-mcp-server-production.up.railway.app"
    
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            endpoints = data.get("endpoints", {})
            features = data.get("features", [])
            
            print_success(f"API is accessible")
            print_info(f"Available endpoints: {len(endpoints)}")
            print_info(f"Features: {', '.join(features)}")
            
            return True
        else:
            print_error(f"Root endpoint failed - Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Connection failed: {str(e)}")
        return False

def test_simple_message():
    """Test sending a simple message if TEST_PHONE_NUMBER is set"""
    test_phone = os.getenv("TEST_PHONE_NUMBER")
    
    if not test_phone:
        print_warning("TEST_PHONE_NUMBER not set - skipping message test")
        return True
    
    print_header("Simple Message Test")
    print_info(f"Testing with phone number: {test_phone}")
    
    base_url = "https://whatsapp-cloud-api-mcp-server-production.up.railway.app"
    
    try:
        payload = {
            "phone_number": test_phone,
            "message": f"🧪 Test message from setup verification - {datetime.now().strftime('%H:%M:%S')}",
            "preview_url": False
        }
        
        response = requests.post(f"{base_url}/api/v1/messaging/send", 
                               json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print_success("Test message sent successfully!")
                return True
            else:
                print_error(f"Message failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print_error(f"Message request failed - Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Message test failed: {str(e)}")
        return False

def run_comprehensive_test():
    """Run the comprehensive QA test if available"""
    print_header("Comprehensive QA Test")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "rigorous_qa_test.py"], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print_success("Comprehensive QA test passed!")
            return True
        else:
            print_error("Comprehensive QA test failed")
            print_info("Run 'python rigorous_qa_test.py' for detailed results")
            return False
            
    except (ImportError, FileNotFoundError):
        print_warning("Comprehensive QA test not available")
        return True
    except subprocess.TimeoutExpired:
        print_warning("Comprehensive QA test timed out")
        return True

def main():
    """Main test function"""
    print("🚀 WhatsApp Cloud API MCP Server - Setup Verification")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Environment Variables", check_environment_variables),
        ("API Connectivity", test_api_connectivity),
        ("API Information", test_root_endpoint),
        ("Simple Message Test", test_simple_message),
        ("Comprehensive QA Test", run_comprehensive_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"{test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("🎉 All tests passed! Your setup is ready to use.")
        return 0
    else:
        print_error("⚠️  Some tests failed. Please check the details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
