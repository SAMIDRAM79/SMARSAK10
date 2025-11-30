from fastapi import APIRouter, HTTPException, status, Depends
from models import Enseignant, EnseignantCreate
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/enseignants", tags=["enseignants"])

@router.post("", response_model=dict)
async def create_enseignant(enseignant: EnseignantCreate, email: str = Depends(verify_email)):
    """Créer un nouvel enseignant"""
    db = get_db()
    
    # Vérifier si le matricule existe
    existing = await db.enseignants.find_one({"matricule": enseignant.matricule})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un enseignant avec ce matricule existe déjà"
        )
    
    enseignant_dict = enseignant.model_dump()
    enseignant_dict["statut"] = "actif"
    
    result = await db.enseignants.insert_one(enseignant_dict)
    
    return {
        "id": str(result.inserted_id),
        "message": "Enseignant créé avec succès"
    }

@router.get("", response_model=List[dict])
async def get_enseignants(email: str = Depends(verify_email)):
    """Récupérer tous les enseignants"""
    db = get_db()
    
    enseignants = await db.enseignants.find({"statut": "actif"}).sort("nom", 1).to_list(100)
    return [serialize_doc(enseignant) for enseignant in enseignants]

@router.get("/{enseignant_id}", response_model=dict)
async def get_enseignant(enseignant_id: str, email: str = Depends(verify_email)):
    """Récupérer un enseignant par son ID"""
    db = get_db()
    
    try:
        enseignant = await db.enseignants.find_one({"_id": ObjectId(enseignant_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID invalide"
        )
    
    if not enseignant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enseignant non trouvé"
        )
    
    return serialize_doc(enseignant)
