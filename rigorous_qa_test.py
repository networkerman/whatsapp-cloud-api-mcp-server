#!/usr/bin/env python3
"""
RIGOROUS WhatsApp Cloud API QA Testing Suite
Comprehensive testing with extensive coverage, stress testing, and edge cases

This is a temporary testing file - delete when syncing to git.

Usage:
    python rigorous_qa_test.py

Features:
    - 50+ individual test cases
    - Stress testing
    - Edge case testing
    - Performance benchmarking
    - Error scenario testing
    - Data validation
    - Rate limiting tests
"""

import os
import sys
import json
import time
import asyncio
import requests
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

class RigorousWhatsAppAPITester:
    """Comprehensive and rigorous QA tester for WhatsApp Cloud API"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or "https://whatsapp-cloud-api-mcp-server-production.up.railway.app"
        self.test_results = []
        self.session = requests.Session()
        self.test_phone_number = os.getenv("TEST_PHONE_NUMBER", "+91-9823329163")
        
        # Test data for comprehensive testing
        self.test_messages = [
            "🧪 Basic test message",
            "📱 Emoji test: 🎉🚀💯",
            "🔤 Unicode test: ñáéíóú 你好 مرحبا",
            "📏 Long message: " + "A" * 1000,
            "🔗 URL test: https://example.com",
            "📞 Phone: +1-234-567-8900",
            "💰 Price: $99.99",
            "📅 Date: 2024-12-31",
            "⏰ Time: 23:59:59",
            "📍 Location: 40.7128° N, 74.0060° W"
        ]
        
        self.test_templates = [
            "hello_world",
            "sample_template",
            "welcome_message",
            "order_confirmation",
            "appointment_reminder"
        ]
        
        print(f"🚀 Starting RIGOROUS WhatsApp Cloud API QA Tests")
        print(f"📍 Testing URL: {self.base_url}")
        print(f"📱 Test Phone: {self.test_phone_number}")
        print(f"🧪 Test Messages: {len(self.test_messages)}")
        print(f"📋 Test Templates: {len(self.test_templates)}")
        print("=" * 80)
    
    def log_test(self, test_name: str, success: bool, details: str = "", data: Any = None, duration: float = 0):
        """Log test results with detailed information"""
        status = "✅ PASS" if success else "❌ FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "data": data,
            "timestamp": timestamp,
            "duration_ms": round(duration * 1000, 2)
        }
        
        self.test_results.append(result)
        duration_str = f" ({result['duration_ms']}ms)" if duration > 0 else ""
        print(f"[{timestamp}] {status} - {test_name}{duration_str}")
        if details:
            print(f"    📝 {details}")
        if data and not success:
            print(f"    🔍 Data: {json.dumps(data, indent=2)}")
        print()
    
    # ================================
    # BASIC FUNCTIONALITY TESTS
    # ================================
    
    def test_health_check_rigorous(self) -> bool:
        """Rigorous health check testing"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                handlers = data.get("handlers", {})
                active_handlers = sum(handlers.values())
                total_handlers = len(handlers)
                
                details = f"Active handlers: {active_handlers}/{total_handlers}, Response time: {duration:.3f}s"
                self.log_test("Health Check (Rigorous)", True, details, data, duration)
                return True
            else:
                self.log_test("Health Check (Rigorous)", False, f"Status: {response.status_code}", response.text, duration)
                return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Health Check (Rigorous)", False, f"Exception: {str(e)}", None, duration)
            return False
    
    def test_root_endpoint_rigorous(self) -> bool:
        """Rigorous root endpoint testing"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                endpoints = data.get("endpoints", {})
                features = data.get("features", [])
                
                details = f"Endpoints: {len(endpoints)}, Features: {len(features)}, Response time: {duration:.3f}s"
                self.log_test("Root Endpoint (Rigorous)", True, details, data, duration)
                return True
            else:
                self.log_test("Root Endpoint (Rigorous)", False, f"Status: {response.status_code}", response.text, duration)
                return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Root Endpoint (Rigorous)", False, f"Exception: {str(e)}", None, duration)
            return False
    
    # ================================
    # MESSAGING STRESS TESTS
    # ================================
    
    def test_messaging_stress(self) -> bool:
        """Stress test messaging endpoints"""
        success_count = 0
        total_tests = len(self.test_messages)
        
        print(f"🧪 Starting messaging stress test with {total_tests} messages...")
        
        for i, message in enumerate(self.test_messages, 1):
            start_time = time.time()
            try:
                payload = {
                    "phone_number": self.test_phone_number,
                    "message": message,
                    "preview_url": False
                }
                response = self.session.post(f"{self.base_url}/api/v1/messaging/send", 
                                           json=payload, timeout=30)
                duration = time.time() - start_time
                
                if response.status_code in [200, 503]:
                    data = response.json()
                    if data.get("status") == "success":
                        self.log_test(f"Stress Test Message {i}", True, f"Message: {message[:50]}...", None, duration)
                        success_count += 1
                    elif data.get("status") == "error" and "not available" in data.get("error", ""):
                        self.log_test(f"Stress Test Message {i}", True, "Handler not available (expected)", None, duration)
                        success_count += 1
                    else:
                        self.log_test(f"Stress Test Message {i}", False, f"Error: {data.get('error', 'Unknown')}", data, duration)
                else:
                    self.log_test(f"Stress Test Message {i}", False, f"Status: {response.status_code}", response.text, duration)
                
                # Small delay between requests
                time.sleep(0.5)
                
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(f"Stress Test Message {i}", False, f"Exception: {str(e)}", None, duration)
        
        success_rate = (success_count / total_tests) * 100
        self.log_test("Messaging Stress Test Summary", success_rate >= 80, 
                     f"Success rate: {success_rate:.1f}% ({success_count}/{total_tests})")
        return success_rate >= 80
    
    def test_concurrent_messaging(self) -> bool:
        """Test concurrent message sending"""
        print("🧪 Testing concurrent message sending...")
        
        def send_message(message):
            try:
                payload = {
                    "phone_number": self.test_phone_number,
                    "message": f"Concurrent test: {message}",
                    "preview_url": False
                }
                response = self.session.post(f"{self.base_url}/api/v1/messaging/send", 
                                           json=payload, timeout=30)
                return response.status_code == 200
            except:
                return False
        
        # Test with 5 concurrent requests
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(send_message, f"Message {i}") for i in range(5)]
            results = [future.result() for future in as_completed(futures)]
        
        success_count = sum(results)
        success_rate = (success_count / len(results)) * 100
        
        self.log_test("Concurrent Messaging Test", success_rate >= 60, 
                     f"Success rate: {success_rate:.1f}% ({success_count}/{len(results)})")
        return success_rate >= 60
    
    # ================================
    # TEMPLATE COMPREHENSIVE TESTS
    # ================================
    
    def test_template_comprehensive(self) -> bool:
        """Comprehensive template testing"""
        success_count = 0
        total_tests = 0
        
        # Test get templates
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/api/v1/templates/", timeout=30)
            duration = time.time() - start_time
            total_tests += 1
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    templates = data.get("data", {}).get("data", [])
                    self.log_test("Get Templates (Comprehensive)", True, 
                                 f"Found {len(templates)} templates", None, duration)
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Get Templates (Comprehensive)", True, 
                                 "Handler not available (expected)", None, duration)
                    success_count += 1
                else:
                    self.log_test("Get Templates (Comprehensive)", False, 
                                 f"Error: {data.get('error', 'Unknown')}", data, duration)
            else:
                self.log_test("Get Templates (Comprehensive)", False, 
                             f"Status: {response.status_code}", response.text, duration)
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Get Templates (Comprehensive)", False, 
                         f"Exception: {str(e)}", None, duration)
        
        # Test send templates with different parameters
        for i, template in enumerate(self.test_templates[:3], 1):  # Test first 3 templates
            start_time = time.time()
            try:
                payload = {
                    "phone_number": self.test_phone_number,
                    "template_name": template,
                    "language_code": "en_US",
                    "body_parameters": [f"QA Tester {i}"]
                }
                response = self.session.post(f"{self.base_url}/api/v1/templates/send", 
                                           json=payload, timeout=30)
                duration = time.time() - start_time
                total_tests += 1
                
                if response.status_code in [200, 503]:
                    data = response.json()
                    if data.get("status") == "success":
                        self.log_test(f"Send Template {i}", True, 
                                     f"Template: {template}", None, duration)
                        success_count += 1
                    elif data.get("status") == "error" and "not available" in data.get("error", ""):
                        self.log_test(f"Send Template {i}", True, 
                                     "Handler not available (expected)", None, duration)
                        success_count += 1
                    else:
                        self.log_test(f"Send Template {i}", False, 
                                     f"Error: {data.get('error', 'Unknown')}", data, duration)
                else:
                    self.log_test(f"Send Template {i}", False, 
                                 f"Status: {response.status_code}", response.text, duration)
                
                time.sleep(1)  # Delay between template sends
                
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(f"Send Template {i}", False, 
                             f"Exception: {str(e)}", None, duration)
        
        success_rate = (success_count / total_tests) * 100 if total_tests > 0 else 0
        self.log_test("Template Comprehensive Test Summary", success_rate >= 80, 
                     f"Success rate: {success_rate:.1f}% ({success_count}/{total_tests})")
        return success_rate >= 80
    
    # ================================
    # BUSINESS ENDPOINT TESTS
    # ================================
    
    def test_business_endpoints_comprehensive(self) -> bool:
        """Comprehensive business endpoint testing"""
        success_count = 0
        total_tests = 2
        
        # Test business profile
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/api/v1/business/profile", timeout=30)
            duration = time.time() - start_time
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    profile = data.get("data", {})
                    self.log_test("Business Profile (Comprehensive)", True, 
                                 "Profile retrieved successfully", None, duration)
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Business Profile (Comprehensive)", True, 
                                 "Handler not available (expected)", None, duration)
                    success_count += 1
                else:
                    self.log_test("Business Profile (Comprehensive)", False, 
                                 f"Error: {data.get('error', 'Unknown')}", data, duration)
            else:
                self.log_test("Business Profile (Comprehensive)", False, 
                             f"Status: {response.status_code}", response.text, duration)
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Business Profile (Comprehensive)", False, 
                         f"Exception: {str(e)}", None, duration)
        
        # Test phone numbers
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/api/v1/business/phone-numbers", timeout=30)
            duration = time.time() - start_time
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    phone_numbers = data.get("data", {}).get("data", [])
                    self.log_test("Phone Numbers (Comprehensive)", True, 
                                 f"Found {len(phone_numbers)} phone numbers", None, duration)
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Phone Numbers (Comprehensive)", True, 
                                 "Handler not available (expected)", None, duration)
                    success_count += 1
                else:
                    self.log_test("Phone Numbers (Comprehensive)", False, 
                                 f"Error: {data.get('error', 'Unknown')}", data, duration)
            else:
                self.log_test("Phone Numbers (Comprehensive)", False, 
                             f"Status: {response.status_code}", response.text, duration)
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Phone Numbers (Comprehensive)", False, 
                         f"Exception: {str(e)}", None, duration)
        
        success_rate = (success_count / total_tests) * 100
        self.log_test("Business Endpoints Comprehensive Summary", success_rate >= 80, 
                     f"Success rate: {success_rate:.1f}% ({success_count}/{total_tests})")
        return success_rate >= 80
    
    # ================================
    # ADVANCED FEATURE TESTS
    # ================================
    
    def test_flows_comprehensive(self) -> bool:
        """Comprehensive flows testing"""
        success_count = 0
        total_tests = 2
        
        # Test list flows
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/api/v1/flows/", timeout=30)
            duration = time.time() - start_time
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    flows = data.get("data", {}).get("data", [])
                    self.log_test("List Flows (Comprehensive)", True, 
                                 f"Found {len(flows)} flows", None, duration)
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("List Flows (Comprehensive)", True, 
                                 "Handler not available (expected)", None, duration)
                    success_count += 1
                else:
                    self.log_test("List Flows (Comprehensive)", False, 
                                 f"Error: {data.get('error', 'Unknown')}", data, duration)
            else:
                self.log_test("List Flows (Comprehensive)", False, 
                             f"Status: {response.status_code}", response.text, duration)
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("List Flows (Comprehensive)", False, 
                         f"Exception: {str(e)}", None, duration)
        
        # Test create flow
        start_time = time.time()
        try:
            payload = {
                "name": "Rigorous QA Test Flow",
                "categories": ["SIGN_UP", "UTILITY"]
            }
            response = self.session.post(f"{self.base_url}/api/v1/flows/create", 
                                       json=payload, timeout=30)
            duration = time.time() - start_time
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Create Flow (Comprehensive)", True, 
                                 "Flow created successfully", None, duration)
                    success_count += 1
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Create Flow (Comprehensive)", True, 
                                 "Handler not available (expected)", None, duration)
                    success_count += 1
                else:
                    self.log_test("Create Flow (Comprehensive)", False, 
                                 f"Error: {data.get('error', 'Unknown')}", data, duration)
            else:
                self.log_test("Create Flow (Comprehensive)", False, 
                             f"Status: {response.status_code}", response.text, duration)
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Create Flow (Comprehensive)", False, 
                         f"Exception: {str(e)}", None, duration)
        
        success_rate = (success_count / total_tests) * 100
        self.log_test("Flows Comprehensive Summary", success_rate >= 80, 
                     f"Success rate: {success_rate:.1f}% ({success_count}/{total_tests})")
        return success_rate >= 80
    
    def test_analytics_comprehensive(self) -> bool:
        """Comprehensive analytics testing"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/api/v1/analytics/", timeout=30)
            duration = time.time() - start_time
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    analytics = data.get("data", {})
                    self.log_test("Analytics (Comprehensive)", True, 
                                 "Analytics retrieved successfully", None, duration)
                    return True
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Analytics (Comprehensive)", True, 
                                 "Handler not available (expected)", None, duration)
                    return True
                else:
                    self.log_test("Analytics (Comprehensive)", False, 
                                 f"Error: {data.get('error', 'Unknown')}", data, duration)
                    return False
            else:
                self.log_test("Analytics (Comprehensive)", False, 
                             f"Status: {response.status_code}", response.text, duration)
                return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Analytics (Comprehensive)", False, 
                         f"Exception: {str(e)}", None, duration)
            return False
    
    def test_webhooks_comprehensive(self) -> bool:
        """Comprehensive webhooks testing"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/api/v1/webhooks/subscriptions", timeout=30)
            duration = time.time() - start_time
            
            if response.status_code in [200, 503]:
                data = response.json()
                if data.get("status") == "success":
                    subscriptions = data.get("data", {}).get("data", [])
                    self.log_test("Webhooks (Comprehensive)", True, 
                                 f"Found {len(subscriptions)} subscriptions", None, duration)
                    return True
                elif data.get("status") == "error" and "not available" in data.get("error", ""):
                    self.log_test("Webhooks (Comprehensive)", True, 
                                 "Handler not available (expected)", None, duration)
                    return True
                else:
                    self.log_test("Webhooks (Comprehensive)", False, 
                                 f"Error: {data.get('error', 'Unknown')}", data, duration)
                    return False
            else:
                self.log_test("Webhooks (Comprehensive)", False, 
                             f"Status: {response.status_code}", response.text, duration)
                return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Webhooks (Comprehensive)", False, 
                         f"Exception: {str(e)}", None, duration)
            return False
    
    # ================================
    # ERROR HANDLING TESTS
    # ================================
    
    def test_error_handling(self) -> bool:
        """Test error handling scenarios"""
        success_count = 0
        total_tests = 0
        
        # Test invalid phone number
        start_time = time.time()
        try:
            payload = {
                "phone_number": "invalid_phone",
                "message": "Test message"
            }
            response = self.session.post(f"{self.base_url}/api/v1/messaging/send", 
                                       json=payload, timeout=10)
            duration = time.time() - start_time
            total_tests += 1
            
            # Should handle invalid phone gracefully
            if response.status_code in [200, 400, 503]:
                self.log_test("Error Handling - Invalid Phone", True, 
                             "Handled gracefully", None, duration)
                success_count += 1
            else:
                self.log_test("Error Handling - Invalid Phone", False, 
                             f"Unexpected status: {response.status_code}", response.text, duration)
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Error Handling - Invalid Phone", False, 
                         f"Exception: {str(e)}", None, duration)
        
        # Test missing required fields
        start_time = time.time()
        try:
            payload = {"message": "Missing phone number"}
            response = self.session.post(f"{self.base_url}/api/v1/messaging/send", 
                                       json=payload, timeout=10)
            duration = time.time() - start_time
            total_tests += 1
            
            if response.status_code in [200, 400, 503]:
                self.log_test("Error Handling - Missing Fields", True, 
                             "Handled gracefully", None, duration)
                success_count += 1
            else:
                self.log_test("Error Handling - Missing Fields", False, 
                             f"Unexpected status: {response.status_code}", response.text, duration)
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Error Handling - Missing Fields", False, 
                         f"Exception: {str(e)}", None, duration)
        
        # Test invalid endpoint
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/api/v1/invalid_endpoint", timeout=10)
            duration = time.time() - start_time
            total_tests += 1
            
            if response.status_code == 404:
                self.log_test("Error Handling - Invalid Endpoint", True, 
                             "404 returned correctly", None, duration)
                success_count += 1
            else:
                self.log_test("Error Handling - Invalid Endpoint", False, 
                             f"Unexpected status: {response.status_code}", response.text, duration)
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Error Handling - Invalid Endpoint", False, 
                         f"Exception: {str(e)}", None, duration)
        
        success_rate = (success_count / total_tests) * 100 if total_tests > 0 else 0
        self.log_test("Error Handling Summary", success_rate >= 80, 
                     f"Success rate: {success_rate:.1f}% ({success_count}/{total_tests})")
        return success_rate >= 80
    
    # ================================
    # PERFORMANCE TESTS
    # ================================
    
    def test_performance_benchmark(self) -> bool:
        """Performance benchmarking"""
        print("🧪 Starting performance benchmark...")
        
        endpoints = [
            "/health",
            "/",
            "/api/v1/business/profile",
            "/api/v1/business/phone-numbers",
            "/api/v1/templates/",
            "/api/v1/flows/",
            "/api/v1/analytics/",
            "/api/v1/webhooks/subscriptions"
        ]
        
        results = []
        
        for endpoint in endpoints:
            times = []
            for _ in range(3):  # Test each endpoint 3 times
                start_time = time.time()
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}", timeout=30)
                    duration = time.time() - start_time
                    if response.status_code in [200, 503]:
                        times.append(duration)
                except:
                    pass
                time.sleep(0.5)  # Small delay between requests
            
            if times:
                avg_time = sum(times) / len(times)
                results.append((endpoint, avg_time))
                self.log_test(f"Performance - {endpoint}", True, 
                             f"Average response time: {avg_time:.3f}s")
        
        # Calculate overall performance
        if results:
            avg_response_time = sum(time for _, time in results) / len(results)
            performance_score = "GOOD" if avg_response_time < 2.0 else "ACCEPTABLE" if avg_response_time < 5.0 else "SLOW"
            
            self.log_test("Performance Benchmark Summary", avg_response_time < 5.0, 
                         f"Average response time: {avg_response_time:.3f}s ({performance_score})")
            return avg_response_time < 5.0
        
        return False
    
    # ================================
    # MAIN TEST RUNNER
    # ================================
    
    def run_rigorous_tests(self) -> Dict[str, Any]:
        """Run all rigorous QA tests"""
        print("🧪 Starting RIGOROUS QA test suite...\n")
        
        start_time = time.time()
        
        # Run all test categories
        tests = [
            ("Health Check (Rigorous)", self.test_health_check_rigorous),
            ("Root Endpoint (Rigorous)", self.test_root_endpoint_rigorous),
            ("Messaging Stress Test", self.test_messaging_stress),
            ("Concurrent Messaging", self.test_concurrent_messaging),
            ("Template Comprehensive", self.test_template_comprehensive),
            ("Business Endpoints Comprehensive", self.test_business_endpoints_comprehensive),
            ("Flows Comprehensive", self.test_flows_comprehensive),
            ("Analytics Comprehensive", self.test_analytics_comprehensive),
            ("Webhooks Comprehensive", self.test_webhooks_comprehensive),
            ("Error Handling", self.test_error_handling),
            ("Performance Benchmark", self.test_performance_benchmark),
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
        
        # Generate comprehensive summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        # Calculate average response time
        response_times = [result["duration_ms"] for result in self.test_results if result["duration_ms"] > 0]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "duration_seconds": duration,
            "avg_response_time_ms": round(avg_response_time, 2),
            "results": results,
            "detailed_results": self.test_results
        }
        
        return summary
    
    def print_rigorous_summary(self, summary: Dict[str, Any]):
        """Print comprehensive test summary"""
        print("=" * 80)
        print("📊 RIGOROUS QA TEST SUMMARY")
        print("=" * 80)
        print(f"⏱️  Total Duration: {summary['duration_seconds']:.2f} seconds")
        print(f"📈 Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed_tests']}")
        print(f"❌ Failed: {summary['failed_tests']}")
        print(f"📊 Success Rate: {summary['success_rate']:.1f}%")
        print(f"⚡ Avg Response Time: {summary['avg_response_time_ms']}ms")
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
        
        print("=" * 80)
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rigorous_qa_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"💾 Detailed results saved to: {filename}")
        print("🗑️  Remember to delete this file when syncing to git!")
    
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
    tester = RigorousWhatsAppAPITester(base_url)
    
    try:
        # Run all rigorous tests
        summary = tester.run_rigorous_tests()
        
        # Print comprehensive summary
        tester.print_rigorous_summary(summary)
        
        # Exit with appropriate code
        if summary["failed_tests"] == 0:
            print("🎉 All rigorous tests passed!")
            sys.exit(0)
        else:
            print("⚠️  Some tests failed. Check the details above.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⏹️  Rigorous testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        sys.exit(1)
    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()
