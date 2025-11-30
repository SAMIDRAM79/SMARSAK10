from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

router = APIRouter(prefix="/centres", tags=["centres"])

@router.post("/")
async def create_centre(
    nom: str,
    capacite_max: int = 480,
    nb_salles_fonctionnelles: int = 16,
    annee_scolaire: str = None,
    email: str = Depends(verify_email)
):
    """Créer un nouveau centre de composition"""
    db = get_db()
    
    # Récupérer l'année scolaire actuelle si non fournie
    if not annee_scolaire:
        params = await db.parametres.find_one()
        annee_scolaire = params.get("annee_scolaire_actuelle", "2024-2025") if params else "2024-2025"
    
    centre = {
        "id": str(uuid4()),
        "nom": nom,
        "capacite_max": capacite_max,
        "nb_salles_fonctionnelles": nb_salles_fonctionnelles,
        "nb_salles_utilisees": 0,
        "nb_candidats": 0,
        "ecoles_affectees": [],
        "annee_scolaire": annee_scolaire
    }
    
    await db.centres_composition.insert_one(centre)
    
    return {
        "message": "Centre créé avec succès",
        "centre": serialize_doc(centre)
    }

@router.get("/")
async def get_centres(annee_scolaire: Optional[str] = None, email: str = Depends(verify_email)):
    """Récupérer tous les centres de composition"""
    db = get_db()
    
    query = {}
    if annee_scolaire:
        query["annee_scolaire"] = annee_scolaire
    
    centres = await db.centres_composition.find(query, {"_id": 0}).sort("nom", 1).to_list(1000)
    return centres

@router.get("/{centre_id}")
async def get_centre(centre_id: str, email: str = Depends(verify_email)):
    """Récupérer un centre spécifique"""
    db = get_db()
    
    centre = await db.centres_composition.find_one({"id": centre_id}, {"_id": 0})
    
    if not centre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Centre non trouvé"
        )
    
    return centre

@router.put("/{centre_id}")
async def update_centre(
    centre_id: str,
    nom: Optional[str] = None,
    capacite_max: Optional[int] = None,
    nb_salles_fonctionnelles: Optional[int] = None,
    email: str = Depends(verify_email)
):
    """Mettre à jour un centre de composition"""
    db = get_db()
    
    update_data = {}
    if nom:
        update_data["nom"] = nom
    if capacite_max is not None:
        update_data["capacite_max"] = capacite_max
    if nb_salles_fonctionnelles is not None:
        update_data["nb_salles_fonctionnelles"] = nb_salles_fonctionnelles
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucune donnée à mettre à jour"
        )
    
    result = await db.centres_composition.update_one(
        {"id": centre_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Centre non trouvé"
        )
    
    return {"message": "Centre mis à jour avec succès"}

@router.delete("/{centre_id}")
async def delete_centre(centre_id: str, email: str = Depends(verify_email)):
    """Supprimer un centre de composition"""
    db = get_db()
    
    result = await db.centres_composition.delete_one({"id": centre_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Centre non trouvé"
        )
    
    return {"message": "Centre supprimé avec succès"}

@router.post("/{centre_id}/affecter-ecole")
async def affecter_ecole_centre(
    centre_id: str,
    codeecole: str,
    email: str = Depends(verify_email)
):
    """Affecter une école à un centre"""
    db = get_db()
    
    # Vérifier que le centre existe
    centre = await db.centres_composition.find_one({"id": centre_id})
    if not centre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Centre non trouvé"
        )
    
    # Vérifier que l'école existe dans les candidats
    ecole = await db.candidats_cepe.find_one({"codeecole": codeecole})
    if not ecole:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="École non trouvée dans les candidats"
        )
    
    # Ajouter l'école au centre si elle n'y est pas déjà
    if codeecole not in centre.get("ecoles_affectees", []):
        await db.centres_composition.update_one(
            {"id": centre_id},
            {"$addToSet": {"ecoles_affectees": codeecole}}
        )
    
    return {"message": "École affectée au centre avec succès"}

@router.delete("/{centre_id}/retirer-ecole/{codeecole}")
async def retirer_ecole_centre(
    centre_id: str,
    codeecole: str,
    email: str = Depends(verify_email)
):
    """Retirer une école d'un centre"""
    db = get_db()
    
    result = await db.centres_composition.update_one(
        {"id": centre_id},
        {"$pull": {"ecoles_affectees": codeecole}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Centre non trouvé"
        )
    
    return {"message": "École retirée du centre avec succès"}
