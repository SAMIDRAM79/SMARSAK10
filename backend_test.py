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

def test_create_student():
    """Test POST /api/students - Create Student"""
    print_test_header("Students API - Create Student")
    
    response = make_request('POST', '/students', TEST_STUDENT)
    if not response:
        print_result(False, "Failed to connect to create student API")
        return False
    
    if response.status_code == 200:
        try:
            result = response.json()
            if 'id' in result and 'message' in result:
                global student_id
                student_id = result['id']
                print_result(True, f"Student creation successful - ID: {student_id}")
                return True
            else:
                print_result(False, "Student creation response missing required fields", str(result))
                return False
        except json.JSONDecodeError:
            print_result(False, "Student creation API returned invalid JSON")
            return False
    elif response.status_code == 400:
        # Student might already exist
        print_result(True, "Student already exists (expected for repeated tests)")
        return True
    else:
        print_result(False, f"Student creation failed with status {response.status_code}", response.text)
        return False

def test_classes_api():
    """Test GET /api/classes"""
    print_test_header("Classes API - List Classes")
    
    response = make_request('GET', '/classes')
    if not response:
        print_result(False, "Failed to connect to classes API")
        return False
    
    if response.status_code == 200:
        try:
            classes = response.json()
            if isinstance(classes, list):
                print_result(True, f"Classes API working - Found {len(classes)} classes")
                return True
            else:
                print_result(False, "Classes API returned invalid format", "Expected list")
                return False
        except json.JSONDecodeError:
            print_result(False, "Classes API returned invalid JSON")
            return False
    else:
        print_result(False, f"Classes API failed with status {response.status_code}", response.text)
        return False

def test_classes_filter_by_niveau():
    """Test Classes API with niveau filter"""
    print_test_header("Classes API - Filter by Niveau")
    
    response = make_request('GET', '/classes?niveau=primaire')
    if not response:
        print_result(False, "Failed to connect to classes API with niveau filter")
        return False
    
    if response.status_code == 200:
        try:
            classes = response.json()
            if isinstance(classes, list):
                print_result(True, f"Classes niveau filter working - Found {len(classes)} primaire classes")
                return True
            else:
                print_result(False, "Classes niveau filter returned invalid format")
                return False
        except json.JSONDecodeError:
            print_result(False, "Classes niveau filter returned invalid JSON")
            return False
    else:
        print_result(False, f"Classes niveau filter failed with status {response.status_code}", response.text)
        return False

def test_matieres_api():
    """Test GET /api/matieres"""
    print_test_header("Matières API - List Subjects")
    
    response = make_request('GET', '/matieres')
    if not response:
        print_result(False, "Failed to connect to matieres API")
        return False
    
    if response.status_code == 200:
        try:
            matieres = response.json()
            if isinstance(matieres, list):
                print_result(True, f"Matières API working - Found {len(matieres)} subjects")
                if matieres:
                    global matiere_id
                    matiere_id = matieres[0].get('id')
                return True
            else:
                print_result(False, "Matières API returned invalid format", "Expected list")
                return False
        except json.JSONDecodeError:
            print_result(False, "Matières API returned invalid JSON")
            return False
    else:
        print_result(False, f"Matières API failed with status {response.status_code}", response.text)
        return False

def test_matieres_filter_by_niveau():
    """Test Matières API with niveau filter"""
    print_test_header("Matières API - Filter by Niveau")
    
    response = make_request('GET', '/matieres?niveau=primaire')
    if not response:
        print_result(False, "Failed to connect to matieres API with niveau filter")
        return False
    
    if response.status_code == 200:
        try:
            matieres = response.json()
            if isinstance(matieres, list):
                print_result(True, f"Matières niveau filter working - Found {len(matieres)} primaire subjects")
                return True
            else:
                print_result(False, "Matières niveau filter returned invalid format")
                return False
        except json.JSONDecodeError:
            print_result(False, "Matières niveau filter returned invalid JSON")
            return False
    else:
        print_result(False, f"Matières niveau filter failed with status {response.status_code}", response.text)
        return False

def test_create_note():
    """Test POST /api/notes - Create Grade"""
    print_test_header("Notes API - Create Grade")
    
    if not student_id or not matiere_id:
        print_result(False, "Missing student_id or matiere_id - skipping note creation")
        return False
    
    test_note = {
        "student_id": student_id,
        "matiere_id": matiere_id,
        "type_examen": "devoir",
        "note": 16.5,
        "note_sur": 20,
        "periode": "trimestre_1",
        "annee_scolaire": "2024-2025",
        "observation": "Très bon travail"
    }
    
    response = make_request('POST', '/notes', test_note)
    if not response:
        print_result(False, "Failed to connect to create note API")
        return False
    
    if response.status_code == 200:
        try:
            result = response.json()
            if 'id' in result and 'message' in result:
                global note_id
                note_id = result['id']
                print_result(True, f"Note creation successful - ID: {note_id}")
                return True
            else:
                print_result(False, "Note creation response missing required fields", str(result))
                return False
        except json.JSONDecodeError:
            print_result(False, "Note creation API returned invalid JSON")
            return False
    else:
        print_result(False, f"Note creation failed with status {response.status_code}", response.text)
        return False

def test_get_student_notes():
    """Test GET /api/notes/student/{student_id}"""
    print_test_header("Notes API - Get Student Notes")
    
    if not student_id:
        print_result(False, "No student_id available - skipping student notes test")
        return False
    
    response = make_request('GET', f'/notes/student/{student_id}')
    if not response:
        print_result(False, "Failed to connect to student notes API")
        return False
    
    if response.status_code == 200:
        try:
            notes = response.json()
            if isinstance(notes, list):
                print_result(True, f"Student notes API working - Found {len(notes)} notes")
                return True
            else:
                print_result(False, "Student notes API returned invalid format")
                return False
        except json.JSONDecodeError:
            print_result(False, "Student notes API returned invalid JSON")
            return False
    else:
        print_result(False, f"Student notes API failed with status {response.status_code}", response.text)
        return False

def test_get_classe_notes():
    """Test GET /api/notes/classe/{classe}"""
    print_test_header("Notes API - Get Class Notes")
    
    response = make_request('GET', '/notes/classe/CP1')
    if not response:
        print_result(False, "Failed to connect to class notes API")
        return False
    
    if response.status_code == 200:
        try:
            notes = response.json()
            if isinstance(notes, list):
                print_result(True, f"Class notes API working - Found {len(notes)} notes")
                return True
            else:
                print_result(False, "Class notes API returned invalid format")
                return False
        except json.JSONDecodeError:
            print_result(False, "Class notes API returned invalid JSON")
            return False
    else:
        print_result(False, f"Class notes API failed with status {response.status_code}", response.text)
        return False

def test_generate_bulletin():
    """Test POST /api/bulletins/generate"""
    print_test_header("Bulletins API - Generate Bulletin")
    
    if not student_id:
        print_result(False, "No student_id available - skipping bulletin generation")
        return False
    
    response = make_request('POST', f'/bulletins/generate?student_id={student_id}&periode=trimestre_1&annee_scolaire=2024-2025')
    if not response:
        print_result(False, "Failed to connect to bulletin generation API")
        return False
    
    if response.status_code == 200:
        try:
            result = response.json()
            if 'id' in result and 'moyenne' in result:
                global bulletin_id
                bulletin_id = result['id']
                print_result(True, f"Bulletin generation successful - Average: {result.get('moyenne')}")
                return True
            else:
                print_result(False, "Bulletin generation response missing required fields", str(result))
                return False
        except json.JSONDecodeError:
            print_result(False, "Bulletin generation API returned invalid JSON")
            return False
    elif response.status_code == 400:
        # No notes found for the period
        print_result(True, "No notes found for bulletin generation (expected for new student)")
        return True
    else:
        print_result(False, f"Bulletin generation failed with status {response.status_code}", response.text)
        return False

def test_get_student_bulletins():
    """Test GET /api/bulletins/student/{student_id}"""
    print_test_header("Bulletins API - Get Student Bulletins")
    
    if not student_id:
        print_result(False, "No student_id available - skipping student bulletins test")
        return False
    
    response = make_request('GET', f'/bulletins/student/{student_id}')
    if not response:
        print_result(False, "Failed to connect to student bulletins API")
        return False
    
    if response.status_code == 200:
        try:
            bulletins = response.json()
            if isinstance(bulletins, list):
                print_result(True, f"Student bulletins API working - Found {len(bulletins)} bulletins")
                return True
            else:
                print_result(False, "Student bulletins API returned invalid format")
                return False
        except json.JSONDecodeError:
            print_result(False, "Student bulletins API returned invalid JSON")
            return False
    else:
        print_result(False, f"Student bulletins API failed with status {response.status_code}", response.text)
        return False

def test_enseignants_api():
    """Test GET /api/enseignants"""
    print_test_header("Enseignants API - List Teachers")
    
    response = make_request('GET', '/enseignants')
    if not response:
        print_result(False, "Failed to connect to enseignants API")
        return False
    
    if response.status_code == 200:
        try:
            enseignants = response.json()
            if isinstance(enseignants, list):
                print_result(True, f"Enseignants API working - Found {len(enseignants)} teachers")
                return True
            else:
                print_result(False, "Enseignants API returned invalid format", "Expected list")
                return False
        except json.JSONDecodeError:
            print_result(False, "Enseignants API returned invalid JSON")
            return False
    else:
        print_result(False, f"Enseignants API failed with status {response.status_code}", response.text)
        return False

def test_statistics_dashboard():
    """Test GET /api/statistics/dashboard"""
    print_test_header("Statistics API - Dashboard")
    
    response = make_request('GET', '/statistics/dashboard')
    if not response:
        print_result(False, "Failed to connect to statistics dashboard API")
        return False
    
    if response.status_code == 200:
        try:
            stats = response.json()
            if 'effectifs' in stats and 'classes' in stats:
                print_result(True, f"Statistics dashboard API working - Total students: {stats['effectifs']['total']}")
                return True
            else:
                print_result(False, "Statistics dashboard response missing required fields", str(stats))
                return False
        except json.JSONDecodeError:
            print_result(False, "Statistics dashboard API returned invalid JSON")
            return False
    else:
        print_result(False, f"Statistics dashboard API failed with status {response.status_code}", response.text)
        return False

def run_all_tests():
    """Run all SMARTSAK10 backend API tests in the specified order"""
    print(f"\n🚀 Starting SMARTSAK10 Backend API Tests")
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Students Listing", test_students_api),
        ("Students Filter by Niveau", test_students_filter_by_niveau),
        ("Students Filter by Classe", test_students_filter_by_classe),
        ("Student Creation", test_create_student),
        ("Classes Listing", test_classes_api),
        ("Classes Filter by Niveau", test_classes_filter_by_niveau),
        ("Matières Listing", test_matieres_api),
        ("Matières Filter by Niveau", test_matieres_filter_by_niveau),
        ("Note Creation", test_create_note),
        ("Student Notes", test_get_student_notes),
        ("Class Notes", test_get_classe_notes),
        ("Bulletin Generation", test_generate_bulletin),
        ("Student Bulletins", test_get_student_bulletins),
        ("Enseignants Listing", test_enseignants_api),
        ("Statistics Dashboard", test_statistics_dashboard),
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
        print("🎉 All SMARTSAK10 backend APIs are working correctly!")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed - backend needs attention")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)