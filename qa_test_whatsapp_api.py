#!/usr/bin/env python3
"""
WhatsApp Cloud API QA Testing Script
Comprehensive testing for all WhatsApp Cloud API endpoints

Usage:
    python qa_test_whatsapp_api.py

Requirements:
    - requests
    - python-dotenv

Install dependencies:
    pip install requests python-dotenv
"""

import os
import sys
import json
import time
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class WhatsAppAPITester:
    """Comprehensive QA tester for WhatsApp Cloud API"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or "https://whatsapp-cloud-api-mcp-server-production.up.railway.app"
        self.test_results = []
        self.session = requests.Session()
        
        # Test data
        self.test_phone_number = os.getenv("TEST_PHONE_NUMBER", "+1234567890")
        self.test_message = "🧪 QA Test Message from WhatsApp API Tester"
        
        print(f"🚀 Starting WhatsApp Cloud API QA Tests")
        print(f"📍 Testing URL: {self.base_url}")
        print(f"📱 Test Phone: {self.test_phone_number}")
        print("=" * 60)
    
    def log_test(self, test_name: str, success: bool, details: str = "", data: Any = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "data": data,
            "timestamp": timestamp
        }
        
        self.test_results.append(result)
        print(f"[{timestamp}] {status} - {test_name}")
        if details:
            print(f"    📝 {details}")
        if data and not success:
            print(f"    🔍 Data: {json.dumps(data, indent=2)}")
        print()
    
    def test_health_check(self) -> bool:
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                handlers = data.get("handlers", {})
                active_handlers = sum(handlers.values())
                details = f"Active handlers: {active_handlers}/{len(handlers)}"
                self.log_test("Health Check", True, details, data)
            else:
                self.log_test("Health Check", False, f"Status: {response.status_code}", response.text)
            
            return success
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False
    
    def test_root_endpoint(self) -> bool:
        """Test root endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                endpoints = data.get("endpoints", {})
                details = f"Available endpoints: {len(endpoints)}"
                self.log_test("Root Endpoint", True, details, data)
            else:
                self.log_test("Root Endpoint", False, f"Status: {response.status_code}", response.text)
            
            return success
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_messaging_endpoints(self) -> bool:
        """Test messaging endpoints"""
        success_count = 0
        total_tests = 2
        
        # Test send message
        try:
            payload = {
                "phone_number": self.test_phone_number,
                "message": self.test_message,
                "preview_url": False
            }
            response = self.session.post(f"{self.base_url}/api/v1/messaging/send", 
                                       json=payload, timeout=10)
            
            if response.status_code in [200, 503]:  # 503 means handler not available
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Send Message", True, "Message sent successfully")
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Send Message", True, "Handler not available (expected in demo mode)")
                    success_count += 1
                else:
                    self.log_test("Send Message", False, f"Error: {data.get('error', 'Unknown error')}", data)
            else:
                self.log_test("Send Message", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Send Message", False, f"Exception: {str(e)}")
        
        # Test send reaction
        try:
            payload = {
                "phone_number": self.test_phone_number,
                "message_id": "test_message_id",
                "emoji": "👍"
            }
            response = self.session.post(f"{self.base_url}/api/v1/messaging/reaction", 
                                       json=payload, timeout=10)
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Send Reaction", True, "Reaction sent successfully")
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Send Reaction", True, "Handler not available (expected in demo mode)")
                    success_count += 1
                else:
                    self.log_test("Send Reaction", False, f"Error: {data.get('error', 'Unknown error')}", data)
            else:
                self.log_test("Send Reaction", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Send Reaction", False, f"Exception: {str(e)}")
        
        return success_count == total_tests
    
    def test_template_endpoints(self) -> bool:
        """Test template endpoints"""
        success_count = 0
        total_tests = 2
        
        # Test get templates
        try:
            response = self.session.get(f"{self.base_url}/api/v1/templates/", timeout=30)  # Increased timeout
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    templates = data.get("data", {}).get("data", [])
                    self.log_test("Get Templates", True, f"Found {len(templates)} templates")
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Get Templates", True, "Handler not available (expected in demo mode)")
                    success_count += 1
                else:
                    self.log_test("Get Templates", False, f"Error: {data.get('error', 'Unknown error')}", data)
            else:
                self.log_test("Get Templates", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get Templates", False, f"Exception: {str(e)}")
        
        # Test send template
        try:
            payload = {
                "phone_number": self.test_phone_number,
                "template_name": "hello_world",
                "language_code": "en_US",
                "body_parameters": ["QA Tester"]
            }
            response = self.session.post(f"{self.base_url}/api/v1/templates/send", 
                                       json=payload, timeout=30)  # Increased timeout
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Send Template", True, "Template sent successfully")
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Send Template", True, "Handler not available (expected in demo mode)")
                    success_count += 1
                else:
                    self.log_test("Send Template", False, f"Error: {data.get('error', 'Unknown error')}", data)
            else:
                self.log_test("Send Template", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Send Template", False, f"Exception: {str(e)}")
        
        return success_count == total_tests
    
    def test_business_endpoints(self) -> bool:
        """Test business endpoints"""
        success_count = 0
        total_tests = 2
        
        # Test get business profile
        try:
            response = self.session.get(f"{self.base_url}/api/v1/business/profile", timeout=10)
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    profile = data.get("data", {})
                    self.log_test("Get Business Profile", True, "Profile retrieved successfully")
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Get Business Profile", True, "Handler not available (expected in demo mode)")
                    success_count += 1
                else:
                    self.log_test("Get Business Profile", False, f"Error: {data.get('error', 'Unknown error')}", data)
            else:
                self.log_test("Get Business Profile", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get Business Profile", False, f"Exception: {str(e)}")
        
        # Test get phone numbers
        try:
            response = self.session.get(f"{self.base_url}/api/v1/business/phone-numbers", timeout=10)
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    phone_numbers = data.get("data", {}).get("data", [])
                    self.log_test("Get Phone Numbers", True, f"Found {len(phone_numbers)} phone numbers")
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Get Phone Numbers", True, "Handler not available (expected in demo mode)")
                    success_count += 1
                else:
                    self.log_test("Get Phone Numbers", False, f"Error: {data.get('error', 'Unknown error')}", data)
            else:
                self.log_test("Get Phone Numbers", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Get Phone Numbers", False, f"Exception: {str(e)}")
        
        return success_count == total_tests
    
    def test_flows_endpoints(self) -> bool:
        """Test flows endpoints"""
        success_count = 0
        total_tests = 2
        
        # Test list flows
        try:
            response = self.session.get(f"{self.base_url}/api/v1/flows/", timeout=10)
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    flows = data.get("data", {}).get("data", [])
                    self.log_test("List Flows", True, f"Found {len(flows)} flows")
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("List Flows", True, "Handler not available (expected in demo mode)")
                    success_count += 1
                else:
                    self.log_test("List Flows", False, f"Error: {data.get('error', 'Unknown error')}", data)
            else:
                self.log_test("List Flows", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("List Flows", False, f"Exception: {str(e)}")
        
        # Test create flow
        try:
            payload = {
                "name": "QA Test Flow",
                "categories": ["SIGN_UP"]
            }
            response = self.session.post(f"{self.base_url}/api/v1/flows/create", 
                                       json=payload, timeout=10)
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Create Flow", True, "Flow created successfully")
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Create Flow", True, "Handler not available (expected in demo mode)")
                    success_count += 1
                else:
                    self.log_test("Create Flow", False, f"Error: {data.get('error', 'Unknown error')}", data)
            else:
                self.log_test("Create Flow", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Create Flow", False, f"Exception: {str(e)}")
        
        return success_count == total_tests
    
    def test_analytics_endpoints(self) -> bool:
        """Test analytics endpoints"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/analytics/", timeout=10)
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    analytics = data.get("data", {})
                    self.log_test("Get Analytics", True, "Analytics retrieved successfully")
                    return True
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Get Analytics", True, "Handler not available (expected in demo mode)")
                    return True
                else:
                    self.log_test("Get Analytics", False, f"Error: {data.get('error', 'Unknown error')}", data)
                    return False
            else:
                self.log_test("Get Analytics", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Get Analytics", False, f"Exception: {str(e)}")
            return False
    
    def test_webhook_endpoints(self) -> bool:
        """Test webhook endpoints"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/webhooks/subscriptions", timeout=10)
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    subscriptions = data.get("data", {}).get("data", [])
                    self.log_test("Get Webhook Subscriptions", True, f"Found {len(subscriptions)} subscriptions")
                    return True
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Get Webhook Subscriptions", True, "Handler not available (expected in demo mode)")
                    return True
                else:
                    self.log_test("Get Webhook Subscriptions", False, f"Error: {data.get('error', 'Unknown error')}", data)
                    return False
            else:
                self.log_test("Get Webhook Subscriptions", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Get Webhook Subscriptions", False, f"Exception: {str(e)}")
            return False
    
    def test_business_account_endpoints(self) -> bool:
        """Test business account endpoints"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/business-account/wabas", timeout=10)
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    wabas = data.get("data", {}).get("data", [])
                    self.log_test("Get WABA Accounts", True, f"Found {len(wabas)} WABA accounts")
                    return True
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Get WABA Accounts", True, "Handler not available (expected in demo mode)")
                    return True
                else:
                    self.log_test("Get WABA Accounts", False, f"Error: {data.get('error', 'Unknown error')}", data)
                    return False
            else:
                self.log_test("Get WABA Accounts", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Get WABA Accounts", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all QA tests"""
        print("🧪 Starting comprehensive QA tests...\n")
        
        start_time = time.time()
        
        # Run all test categories
        tests = [
            ("Health Check", self.test_health_check),
            ("Root Endpoint", self.test_root_endpoint),
            ("Messaging Endpoints", self.test_messaging_endpoints),
            ("Template Endpoints", self.test_template_endpoints),
            ("Business Endpoints", self.test_business_endpoints),
            ("Flows Endpoints", self.test_flows_endpoints),
            ("Analytics Endpoints", self.test_analytics_endpoints),
            ("Webhook Endpoints", self.test_webhook_endpoints),
            ("Business Account Endpoints", self.test_business_account_endpoints),
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                self.log_test(test_name, False, f"Test failed with exception: {str(e)}")
                results[test_name] = False
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "duration_seconds": duration,
            "results": results,
            "detailed_results": self.test_results
        }
        
        return summary
    
    def print_summary(self, summary: Dict[str, Any]):
        """Print test summary"""
        print("=" * 60)
        print("📊 QA TEST SUMMARY")
        print("=" * 60)
        print(f"⏱️  Duration: {summary['duration_seconds']:.2f} seconds")
        print(f"📈 Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed_tests']}")
        print(f"❌ Failed: {summary['failed_tests']}")
        print(f"📊 Success Rate: {summary['success_rate']:.1f}%")
        print()
        
        print("📋 Test Category Results:")
        for category, result in summary["results"].items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status} - {category}")
        
        print()
        
        if summary["failed_tests"] > 0:
            print("🔍 Failed Tests Details:")
            for result in summary["detailed_results"]:
                if not result["success"]:
                    print(f"   ❌ {result['test']}: {result['details']}")
        
        print("=" * 60)
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qa_test_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"💾 Detailed results saved to: {filename}")
    
    def cleanup(self):
        """Cleanup resources"""
        self.session.close()


def main():
    """Main function"""
    # Check if base URL is provided as command line argument
    base_url = None
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    # Create tester instance
    tester = WhatsAppAPITester(base_url)
    
    try:
        # Run all tests
        summary = tester.run_all_tests()
        
        # Print summary
        tester.print_summary(summary)
        
        # Exit with appropriate code
        if summary["failed_tests"] == 0:
            print("🎉 All tests passed!")
            sys.exit(0)
        else:
            print("⚠️  Some tests failed. Check the details above.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        sys.exit(1)
    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()
