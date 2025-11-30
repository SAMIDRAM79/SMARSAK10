from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import List
from uuid import uuid4
import pandas as pd
import io

router = APIRouter(prefix="/secteurs", tags=["secteurs"])

@router.post("/import/excel")
async def import_secteurs_excel(
    file: UploadFile = File(...),
    annee_scolaire: str = Form(...),
    email: str = Depends(verify_email)
):
    """Importer les secteurs et leurs écoles depuis un fichier Excel (2 colonnes: SECTEUR | ÉCOLES)"""
    db = get_db()
    
    try:
        contents = await file.read()
        
        try:
            df = pd.read_excel(io.BytesIO(contents))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erreur lors de la lecture du fichier Excel: {str(e)}"
            )
        
        # Vérifier les colonnes
        if len(df.columns) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le fichier doit contenir au moins 2 colonnes (SECTEUR et ÉCOLES)"
            )
        
        # Renommer les colonnes pour uniformiser
        df.columns = ['secteur', 'ecole'] + list(df.columns[2:])
        
        secteurs_importes = 0
        
        # Grouper par secteur
        for secteur_nom, group in df.groupby('secteur'):
            ecoles = group['ecole'].tolist()
            
            # Chercher si le secteur existe déjà
            existing = await db.secteurs_pedagogiques.find_one({
                "nom": str(secteur_nom),
                "annee_scolaire": annee_scolaire
            })
            
            if existing:
                # Mettre à jour les écoles
                await db.secteurs_pedagogiques.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {"ecoles": [str(e) for e in ecoles]}}
                )
            else:
                # Créer nouveau secteur
                secteur_doc = {
                    "id": str(uuid4()),
                    "nom": str(secteur_nom),
                    "ecoles": [str(e) for e in ecoles],
                    "annee_scolaire": annee_scolaire
                }
                await db.secteurs_pedagogiques.insert_one(secteur_doc)
            
            secteurs_importes += 1
        
        return {
            "message": "Import réussi",
            "secteurs_importes": secteurs_importes,
            "total_ecoles": len(df)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'importation: {str(e)}"
        )

@router.get("/")
async def get_secteurs(annee_scolaire: str = None, email: str = Depends(verify_email)):
    """Récupérer tous les secteurs pédagogiques"""
    db = get_db()
    
    query = {}
    if annee_scolaire:
        query["annee_scolaire"] = annee_scolaire
    
    secteurs = await db.secteurs_pedagogiques.find(query, {"_id": 0}).sort("nom", 1).to_list(1000)
    return secteurs

@router.post("/")
async def create_secteur(
    nom: str,
    annee_scolaire: str,
    email: str = Depends(verify_email)
):
    """Créer un nouveau secteur pédagogique"""
    db = get_db()
    
    secteur = {
        "id": str(uuid4()),
        "nom": nom,
        "ecoles": [],
        "annee_scolaire": annee_scolaire
    }
    
    await db.secteurs_pedagogiques.insert_one(secteur)
    
    return {
        "message": "Secteur créé avec succès",
        "secteur": serialize_doc(secteur)
    }

@router.post("/{secteur_id}/ajouter-ecole")
async def ajouter_ecole_secteur(
    secteur_id: str,
    ecole: str,
    email: str = Depends(verify_email)
):
    """Ajouter une école à un secteur"""
    db = get_db()
    
    result = await db.secteurs_pedagogiques.update_one(
        {"id": secteur_id},
        {"$addToSet": {"ecoles": ecole}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Secteur non trouvé"
        )
    
    return {"message": "École ajoutée au secteur avec succès"}

@router.delete("/{secteur_id}/retirer-ecole")
async def retirer_ecole_secteur(
    secteur_id: str,
    ecole: str,
    email: str = Depends(verify_email)
):
    """Retirer une école d'un secteur"""
    db = get_db()
    
    result = await db.secteurs_pedagogiques.update_one(
        {"id": secteur_id},
        {"$pull": {"ecoles": ecole}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Secteur non trouvé"
        )
    
    return {"message": "École retirée du secteur avec succès"}
