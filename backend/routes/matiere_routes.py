from fastapi import APIRouter, HTTPException, status, Depends
from models import Matiere, MatiereCreate
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/matieres", tags=["matieres"])

@router.post("", response_model=dict)
async def create_matiere(matiere: MatiereCreate, email: str = Depends(verify_email)):
    """Créer une nouvelle matière"""
    db = get_db()
    
    matiere_dict = matiere.model_dump()
    result = await db.matieres.insert_one(matiere_dict)
    
    return {
        "id": str(result.inserted_id),
        "message": "Matière créée avec succès"
    }

@router.get("", response_model=List[dict])
async def get_matieres(email: str = Depends(verify_email), niveau: str = None):
    """Récupérer toutes les matières"""
    db = get_db()
    
    query = {}
    if niveau:
        query["niveau"] = niveau
    
    matieres = await db.matieres.find(query).sort("nom", 1).to_list(100)
    return [serialize_doc(matiere) for matiere in matieres]

@router.get("/{matiere_id}", response_model=dict)
async def get_matiere(matiere_id: str, email: str = Depends(verify_email)):
    """Récupérer une matière par son ID"""
    db = get_db()
    
    try:
        matiere = await db.matieres.find_one({"_id": ObjectId(matiere_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID invalide"
        )
    
    if not matiere:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matière non trouvée"
        )
    
    return serialize_doc(matiere)
