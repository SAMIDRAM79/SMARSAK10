from fastapi import APIRouter, HTTPException, status, Depends
from models import Student, StudentCreate, StudentLevel
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import List
from bson import ObjectId
from datetime import datetime, date

router = APIRouter(prefix="/students", tags=["students"])

@router.post("", response_model=dict)
async def create_student(student: StudentCreate, email: str = Depends(verify_email)):
    """Créer un nouvel élève"""
    db = get_db()
    
    # Vérifier si le matricule existe déjà
    existing = await db.students.find_one({"matricule": student.matricule})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un élève avec ce matricule existe déjà"
        )
    
    # Créer l'élève
    student_dict = student.model_dump()
    # Convert date to string for MongoDB compatibility
    if isinstance(student_dict.get("date_naissance"), date):
        student_dict["date_naissance"] = student_dict["date_naissance"].isoformat()
    student_dict["annee_scolaire"] = "2024-2025"
    student_dict["date_inscription"] = datetime.utcnow()
    student_dict["statut"] = "actif"
    
    result = await db.students.insert_one(student_dict)
    
    # Mettre à jour l'effectif de la classe
    await db.classes.update_one(
        {"nom": student.classe},
        {"$inc": {"effectif_actuel": 1}}
    )
    
    return {
        "id": str(result.inserted_id),
        "message": "Élève créé avec succès"
    }

@router.get("", response_model=List[dict])
async def get_students(email: str = Depends(verify_email), niveau: str = None, classe: str = None):
    """Récupérer tous les élèves avec filtres optionnels"""
    db = get_db()
    
    query = {"statut": "actif"}
    if niveau:
        query["niveau"] = niveau
    if classe:
        query["classe"] = classe
    
    students = await db.students.find(query).sort("nom", 1).to_list(1000)
    return [serialize_doc(student) for student in students]

@router.get("/{student_id}", response_model=dict)
async def get_student(student_id: str, email: str = Depends(verify_email)):
    """Récupérer un élève par son ID"""
    db = get_db()
    
    try:
        student = await db.students.find_one({"_id": ObjectId(student_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID invalide"
        )
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Élève non trouvé"
        )
    
    return serialize_doc(student)

@router.put("/{student_id}", response_model=dict)
async def update_student(student_id: str, student: StudentCreate, email: str = Depends(verify_email)):
    """Mettre à jour un élève"""
    db = get_db()
    
    try:
        result = await db.students.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": student.model_dump()}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID invalide"
        )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Élève non trouvé"
        )
    
    return {"message": "Élève mis à jour avec succès"}

@router.delete("/{student_id}")
async def delete_student(student_id: str, email: str = Depends(verify_email)):
    """Supprimer un élève (désactivation)"""
    db = get_db()
    
    try:
        result = await db.students.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": {"statut": "inactif"}}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID invalide"
        )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Élève non trouvé"
        )
    
    return {"message": "Élève désactivé avec succès"}
