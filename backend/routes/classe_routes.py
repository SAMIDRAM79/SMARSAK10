from fastapi import APIRouter, HTTPException, status, Depends
from models import Classe, ClasseCreate
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/classes", tags=["classes"])

@router.post("", response_model=dict)
async def create_classe(classe: ClasseCreate, email: str = Depends(verify_email)):
    """Créer une nouvelle classe"""
    db = get_db()
    
    # Vérifier si la classe existe déjà
    existing = await db.classes.find_one({
        "nom": classe.nom,
        "annee_scolaire": classe.annee_scolaire
    })
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Une classe avec ce nom existe déjà pour cette année"
        )
    
    classe_dict = classe.model_dump()
    classe_dict["effectif_actuel"] = 0
    
    result = await db.classes.insert_one(classe_dict)
    
    return {
        "id": str(result.inserted_id),
        "message": "Classe créée avec succès"
    }

@router.get("", response_model=List[dict])
async def get_classes(email: str = Depends(verify_email), niveau: str = None):
    """Récupérer toutes les classes"""
    db = get_db()
    
    query = {}
    if niveau:
        query["niveau"] = niveau
    
    classes = await db.classes.find(query).sort("nom", 1).to_list(100)
    return [serialize_doc(classe) for classe in classes]

@router.get("/{classe_id}", response_model=dict)
async def get_classe(classe_id: str, email: str = Depends(verify_email)):
    """Récupérer une classe par son ID"""
    db = get_db()
    
    try:
        classe = await db.classes.find_one({"_id": ObjectId(classe_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID invalide"
        )
    
    if not classe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classe non trouvée"
        )
    
    return serialize_doc(classe)
