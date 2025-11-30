from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/parametres", tags=["parametres"])

@router.get("/")
async def get_parametres(email: str = Depends(verify_email)):
    """Récupérer les paramètres globaux de l'application"""
    db = get_db()
    
    params = await db.parametres.find_one()
    
    if not params:
        # Créer des paramètres par défaut
        default_params = {
            "annee_scolaire_actuelle": "2024-2025",
            "session_examen": "2025",
            "drena": "BOUAKE 2",
            "iepp": "SAKASSOU",
            "region": "GBEKE",
            "date_examen": None,
            "logo_url": "/logo.jpg"
        }
        result = await db.parametres.insert_one(default_params)
        params = await db.parametres.find_one({"_id": result.inserted_id})
    
    return serialize_doc(params)

@router.put("/")
async def update_parametres(
    annee_scolaire_actuelle: Optional[str] = None,
    session_examen: Optional[str] = None,
    drena: Optional[str] = None,
    iepp: Optional[str] = None,
    region: Optional[str] = None,
    date_examen: Optional[str] = None,
    email: str = Depends(verify_email)
):
    """Mettre à jour les paramètres globaux"""
    db = get_db()
    
    # Construire le dictionnaire de mise à jour
    update_data = {}
    if annee_scolaire_actuelle:
        update_data["annee_scolaire_actuelle"] = annee_scolaire_actuelle
    if session_examen:
        update_data["session_examen"] = session_examen
    if drena:
        update_data["drena"] = drena
    if iepp:
        update_data["iepp"] = iepp
    if region:
        update_data["region"] = region
    if date_examen:
        update_data["date_examen"] = date_examen
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucun paramètre à mettre à jour"
        )
    
    # Vérifier si des paramètres existent
    existing = await db.parametres.find_one()
    
    if existing:
        # Mettre à jour
        await db.parametres.update_one(
            {"_id": existing["_id"]},
            {"$set": update_data}
        )
    else:
        # Créer
        await db.parametres.insert_one(update_data)
    
    return {
        "message": "Paramètres mis à jour avec succès",
        "updated": update_data
    }
