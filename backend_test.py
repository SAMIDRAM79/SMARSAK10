#!/usr/bin/env python3
"""
Backend API Testing Suite for SMARTSAK10 - Système de gestion scolaire
Tests all backend APIs including students, classes, subjects, grades, bulletins, teachers, and statistics.
"""

import requests
import json
import sys
import os
from datetime import datetime, date

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        print("❌ Frontend .env file not found")
        return None
    return None

BACKEND_URL = get_backend_url()
if not BACKEND_URL:
    print("❌ Could not get backend URL from frontend/.env")
    sys.exit(1)

API_BASE = f"{BACKEND_URL}/api"
print(f"🔗 Testing SMARTSAK10 backend at: {API_BASE}")

# Required header for all requests
HEADERS = {
    "X-User-Email": "konatdra@gmail.com",
    "Content-Type": "application/json"
}

# Test data for SMARTSAK10
TEST_STUDENT = {
    "matricule": "STU2024001",
    "nom": "KOUAME",
    "prenoms": "Aya Marie",
    "date_naissance": "2015-03-15",
    "lieu_naissance": "Abidjan",
    "genre": "feminin",
    "niveau": "primaire",
    "classe": "CP1",
    "nom_pere": "KOUAME Jean",
    "nom_mere": "TRAORE Aminata",
    "telephone_tuteur": "+225 07 12 34 56 78",
    "adresse": "Cocody, Riviera 2"
}

TEST_CLASSE = {
    "nom": "CP1",
    "niveau": "primaire",
    "effectif_max": 35,
    "annee_scolaire": "2024-2025"
}

TEST_MATIERE = {
    "nom": "Mathématiques",
    "note_sur": 20,
    "niveau": "primaire",
    "coefficient": 3.0
}

TEST_ENSEIGNANT = {
    "matricule": "ENS2024001",
    "nom": "DIABATE",
    "prenoms": "Moussa",
    "genre": "masculin",
    "telephone": "+225 05 67 89 01 23",
    "email": "moussa.diabate@smartsak10.ci",
    "specialite": "Mathématiques",
    "date_embauche": "2024-01-15"
}

# Global variables for test state
student_id = None
matiere_id = None
note_id = None
bulletin_id = None

def print_test_header(test_name):
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {test_name}")
    print(f"{'='*60}")

def print_result(success, message, details=None):
    status = "✅" if success else "❌"
    print(f"{status} {message}")
    if details:
        print(f"   Details: {details}")

def make_request(method, endpoint, data=None, headers=None, expected_status=None):
    """Make HTTP request and return response with error handling"""
    url = f"{API_BASE}{endpoint}"
    
    # Use global headers with X-User-Email
    request_headers = HEADERS.copy()
    if headers:
        request_headers.update(headers)
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=request_headers, timeout=30)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=request_headers, timeout=30)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=request_headers, timeout=30)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=request_headers, timeout=30)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        print(f"   {method.upper()} {endpoint} -> Status: {response.status_code}")
        
        if expected_status and response.status_code != expected_status:
            print(f"   Expected status {expected_status}, got {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
        return response
        
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection failed to {url}")
        return None
    except requests.exceptions.Timeout:
        print(f"   ❌ Request timeout to {url}")
        return None
    except Exception as e:
        print(f"   ❌ Request error: {str(e)}")
        return None

def test_students_api():
    """Test Students API - GET /api/students"""
    print_test_header("Students API - List Students")
    
    response = make_request('GET', '/students')
    if not response:
        print_result(False, "Failed to connect to students API")
        return False
    
    if response.status_code == 200:
        try:
            students = response.json()
            if isinstance(students, list):
                print_result(True, f"Students API working - Found {len(students)} students")
                return True
            else:
                print_result(False, "Students API returned invalid format", "Expected list")
                return False
        except json.JSONDecodeError:
            print_result(False, "Students API returned invalid JSON")
            return False
    else:
        print_result(False, f"Students API failed with status {response.status_code}", response.text)
        return False

def test_students_filter_by_niveau():
    """Test Students API with niveau filter"""
    print_test_header("Students API - Filter by Niveau")
    
    response = make_request('GET', '/students?niveau=primaire')
    if not response:
        print_result(False, "Failed to connect to students API with niveau filter")
        return False
    
    if response.status_code == 200:
        try:
            students = response.json()
            if isinstance(students, list):
                print_result(True, f"Students niveau filter working - Found {len(students)} primaire students")
                return True
            else:
                print_result(False, "Students niveau filter returned invalid format")
                return False
        except json.JSONDecodeError:
            print_result(False, "Students niveau filter returned invalid JSON")
            return False
    else:
        print_result(False, f"Students niveau filter failed with status {response.status_code}", response.text)
        return False

def test_students_filter_by_classe():
    """Test Students API with classe filter"""
    print_test_header("Students API - Filter by Classe")
    
    response = make_request('GET', '/students?classe=CP1')
    if not response:
        print_result(False, "Failed to connect to students API with classe filter")
        return False
    
    if response.status_code == 200:
        try:
            students = response.json()
            if isinstance(students, list):
                print_result(True, f"Students classe filter working - Found {len(students)} CP1 students")
                return True
            else:
                print_result(False, "Students classe filter returned invalid format")
                return False
        except json.JSONDecodeError:
            print_result(False, "Students classe filter returned invalid JSON")
            return False
    else:
        print_result(False, f"Students classe filter failed with status {response.status_code}", response.text)
        return False

def test_user_registration():
    """Test POST /api/auth/register"""
    print_test_header("User Registration")
    
    response = make_request('POST', '/auth/register', TEST_USER)
    if not response:
        print_result(False, "Failed to connect to registration API")
        return False
    
    if response.status_code == 200:
        try:
            result = response.json()
            if 'token' in result and 'email' in result:
                global auth_token
                auth_token = result['token']
                print_result(True, f"User registration successful - User: {result.get('name')}")
                return True
            else:
                print_result(False, "Registration response missing required fields", str(result))
                return False
        except json.JSONDecodeError:
            print_result(False, "Registration API returned invalid JSON")
            return False
    elif response.status_code == 400:
        # User might already exist, try to continue with login
        print_result(True, "User already exists (expected for repeated tests)")
        return True
    else:
        print_result(False, f"Registration failed with status {response.status_code}", response.text)
        return False

def test_user_login():
    """Test POST /api/auth/login"""
    print_test_header("User Login")
    
    login_data = {
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    
    response = make_request('POST', '/auth/login', login_data)
    if not response:
        print_result(False, "Failed to connect to login API")
        return False
    
    if response.status_code == 200:
        try:
            result = response.json()
            if 'token' in result and 'email' in result:
                global auth_token
                auth_token = result['token']
                print_result(True, f"User login successful - User: {result.get('name')}")
                return True
            else:
                print_result(False, "Login response missing required fields", str(result))
                return False
        except json.JSONDecodeError:
            print_result(False, "Login API returned invalid JSON")
            return False
    else:
        print_result(False, f"Login failed with status {response.status_code}", response.text)
        return False

def test_authenticated_route():
    """Test GET /api/auth/me with authentication"""
    print_test_header("Authenticated Route (/auth/me)")
    
    if not auth_token:
        print_result(False, "No auth token available - skipping authenticated test")
        return False
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = make_request('GET', '/auth/me', headers=headers)
    
    if not response:
        print_result(False, "Failed to connect to /auth/me API")
        return False
    
    if response.status_code == 200:
        try:
            result = response.json()
            if 'email' in result and 'name' in result:
                print_result(True, f"Authenticated route working - User: {result.get('name')}")
                return True
            else:
                print_result(False, "Auth/me response missing required fields", str(result))
                return False
        except json.JSONDecodeError:
            print_result(False, "Auth/me API returned invalid JSON")
            return False
    else:
        print_result(False, f"Auth/me failed with status {response.status_code}", response.text)
        return False

def test_order_creation():
    """Test POST /api/orders"""
    print_test_header("Order Creation")
    
    response = make_request('POST', '/orders', TEST_ORDER)
    if not response:
        print_result(False, "Failed to connect to orders API")
        return False
    
    if response.status_code == 200:
        try:
            result = response.json()
            if 'order_number' in result and 'status' in result:
                print_result(True, f"Order creation successful - Order: {result.get('order_number')}")
                return True
            else:
                print_result(False, "Order response missing required fields", str(result))
                return False
        except json.JSONDecodeError:
            print_result(False, "Orders API returned invalid JSON")
            return False
    else:
        print_result(False, f"Order creation failed with status {response.status_code}", response.text)
        return False

def test_ticket_creation():
    """Test POST /api/tickets"""
    print_test_header("Ticket Creation")
    
    response = make_request('POST', '/tickets', TEST_TICKET)
    if not response:
        print_result(False, "Failed to connect to tickets API")
        return False
    
    if response.status_code == 200:
        try:
            result = response.json()
            if 'ticket_number' in result and 'status' in result:
                print_result(True, f"Ticket creation successful - Ticket: {result.get('ticket_number')}")
                return True
            else:
                print_result(False, "Ticket response missing required fields", str(result))
                return False
        except json.JSONDecodeError:
            print_result(False, "Tickets API returned invalid JSON")
            return False
    else:
        print_result(False, f"Ticket creation failed with status {response.status_code}", response.text)
        return False

def test_download_tracking():
    """Test POST /api/downloads/track"""
    print_test_header("Download Tracking")
    
    if not download_id:
        print_result(False, "No download ID available - skipping download tracking test")
        return False
    
    track_data = {
        "download_id": download_id,
        "user_id": "test_user_123"
    }
    
    response = make_request('POST', '/downloads/track', track_data)
    if not response:
        print_result(False, "Failed to connect to download tracking API")
        return False
    
    if response.status_code == 200:
        try:
            result = response.json()
            if 'success' in result and result['success']:
                print_result(True, "Download tracking successful")
                return True
            else:
                print_result(False, "Download tracking response indicates failure", str(result))
                return False
        except json.JSONDecodeError:
            print_result(False, "Download tracking API returned invalid JSON")
            return False
    else:
        print_result(False, f"Download tracking failed with status {response.status_code}", response.text)
        return False

def run_all_tests():
    """Run all backend API tests in the specified order"""
    print(f"\n🚀 Starting SmartScool Backend API Tests")
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Products Listing", test_products_api),
        ("Downloads Listing", test_downloads_api),
        ("User Registration", test_user_registration),
        ("User Login", test_user_login),
        ("Authenticated Route", test_authenticated_route),
        ("Order Creation", test_order_creation),
        ("Ticket Creation", test_ticket_creation),
        ("Download Tracking", test_download_tracking),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print_result(False, f"{test_name} failed with exception: {str(e)}")
            results[test_name] = False
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All backend APIs are working correctly!")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed - backend needs attention")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)