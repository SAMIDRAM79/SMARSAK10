#!/usr/bin/env python3
"""
Comprehensive Test Scenario for SMARTSAK10
Tests the complete workflow: Students -> Subjects -> Grades -> Bulletins -> Statistics
"""

import requests
import json
import sys
from datetime import datetime

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
API_BASE = f"{BACKEND_URL}/api"

# Required header for all requests
HEADERS = {
    "X-User-Email": "konatdra@gmail.com",
    "Content-Type": "application/json"
}

def make_request(method, endpoint, data=None):
    """Make HTTP request and return response"""
    url = f"{API_BASE}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=HEADERS, timeout=30)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=HEADERS, timeout=30)
        
        print(f"   {method.upper()} {endpoint} -> Status: {response.status_code}")
        return response
        
    except Exception as e:
        print(f"   ❌ Request error: {str(e)}")
        return None

def run_comprehensive_test():
    """Run comprehensive test scenario"""
    print(f"\n🚀 SMARTSAK10 Comprehensive Test Scenario")
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Get existing students
    print(f"\n📋 Step 1: Récupérer les élèves existants")
    response = make_request('GET', '/students')
    if response and response.status_code == 200:
        students = response.json()
        print(f"✅ Found {len(students)} students")
        if students:
            student_id = students[0]['id']
            print(f"   Using student: {students[0]['nom']} {students[0]['prenoms']}")
        else:
            print("❌ No students found")
            return False
    else:
        print("❌ Failed to get students")
        return False
    
    # Step 2: Get subjects
    print(f"\n📚 Step 2: Récupérer les matières")
    response = make_request('GET', '/matieres')
    if response and response.status_code == 200:
        matieres = response.json()
        print(f"✅ Found {len(matieres)} subjects")
        if matieres:
            matiere_id = matieres[0]['id']
            print(f"   Using subject: {matieres[0]['nom']}")
        else:
            print("❌ No subjects found")
            return False
    else:
        print("❌ Failed to get subjects")
        return False
    
    # Step 3: Create some grades
    print(f"\n📝 Step 3: Créer quelques notes pour l'élève")
    
    # Create multiple grades for different subjects
    grades_created = 0
    for i, matiere in enumerate(matieres[:3]):  # Test with first 3 subjects
        note_data = {
            "student_id": student_id,
            "matiere_id": matiere['id'],
            "type_examen": "devoir",
            "note": 15.0 + i,  # Different grades: 15, 16, 17
            "note_sur": 20,
            "periode": "trimestre_1",
            "annee_scolaire": "2024-2025",
            "observation": f"Test note for {matiere['nom']}"
        }
        
        response = make_request('POST', '/notes', note_data)
        if response and response.status_code == 200:
            grades_created += 1
            print(f"   ✅ Created grade {15.0 + i}/20 for {matiere['nom']}")
        else:
            print(f"   ❌ Failed to create grade for {matiere['nom']}")
    
    print(f"✅ Created {grades_created} grades")
    
    # Step 4: Generate bulletin
    print(f"\n📊 Step 4: Générer un bulletin")
    response = make_request('POST', f'/bulletins/generate?student_id={student_id}&periode=trimestre_1&annee_scolaire=2024-2025')
    if response and response.status_code == 200:
        bulletin = response.json()
        print(f"✅ Bulletin generated successfully")
        print(f"   Average: {bulletin['moyenne']}/20")
        print(f"   Rank: {bulletin['rang']}")
        print(f"   Appreciation: {bulletin['appreciation']}")
    else:
        print("❌ Failed to generate bulletin")
        return False
    
    # Step 5: Check statistics
    print(f"\n📈 Step 5: Vérifier les statistiques")
    response = make_request('GET', '/statistics/dashboard')
    if response and response.status_code == 200:
        stats = response.json()
        print(f"✅ Statistics retrieved successfully")
        print(f"   Total students: {stats['effectifs']['total']}")
        print(f"   Total classes: {stats['classes']['total']}")
        print(f"   Total teachers: {stats['personnel']['enseignants']}")
        print(f"   School year: {stats['annee_scolaire']}")
    else:
        print("❌ Failed to get statistics")
        return False
    
    # Additional verification: Get student notes
    print(f"\n🔍 Verification: Vérifier les notes de l'élève")
    response = make_request('GET', f'/notes/student/{student_id}')
    if response and response.status_code == 200:
        notes = response.json()
        print(f"✅ Student has {len(notes)} notes")
        for note in notes:
            print(f"   {note.get('matiere_nom', 'Unknown')}: {note['note']}/{note['note_sur']}")
    else:
        print("❌ Failed to get student notes")
        return False
    
    print(f"\n🎉 Comprehensive test completed successfully!")
    print(f"✅ All SMARTSAK10 APIs are working correctly in the complete workflow")
    return True

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)