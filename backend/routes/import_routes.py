from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import List, Optional
from datetime import datetime, date
import pandas as pd
import io
import zipfile
import os
from pathlib import Path
import shutil
from uuid import uuid4

router = APIRouter(prefix="/import", tags=["import"])

# Dossier pour stocker les photos
UPLOAD_DIR = Path("/app/backend/uploads/photos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/excel/candidats")
async def import_candidats_excel(
    file: UploadFile = File(...),
    annee_scolaire: str = Form(...),
    email: str = Depends(verify_email)
):
    """Importer les candidats depuis un fichier Excel AGCEPE/DECO"""
    db = get_db()
    
    try:
        # Lire le fichier Excel
        contents = await file.read()
        
        # Essayer de lire avec pandas
        try:
            df = pd.read_excel(io.BytesIO(contents))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erreur lors de la lecture du fichier Excel: {str(e)}"
            )
        
        # Vérifier les colonnes requises
        colonnes_requises = [
            'codedren', 'codeiep', 'iep', 'codeecole', 'ecole', 'matricule',
            'nom', 'prenoms', 'sexe', 'jour', 'mois', 'annee', 'nationalite',
            'localite', 'codesp', 'sp', 'niveau'
        ]
        
        colonnes_manquantes = [col for col in colonnes_requises if col not in df.columns]
        if colonnes_manquantes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Colonnes manquantes dans le fichier: {', '.join(colonnes_manquantes)}"
            )
        
        # Traiter chaque ligne
        candidats_importes = []
        candidats_erreurs = []
        
        for index, row in df.iterrows():
            try:
                # Construire la date de naissance
                jour = int(row['jour'])
                mois = int(row['mois'])
                annee = int(row['annee'])
                date_naissance = date(annee, mois, jour)
                
                # Préparer le document candidat
                candidat = {
                    "id": str(uuid4()),
                    "codedren": str(row['codedren']),
                    "codeiep": str(row['codeiep']),
                    "iep": str(row['iep']),
                    "codeecole": str(row['codeecole']),
                    "ecole": str(row['ecole']),
                    "matricule": str(row['matricule']),
                    "nom": str(row['nom']).upper(),
                    "prenoms": str(row['prenoms']).title(),
                    "sexe": str(row['sexe']).upper(),
                    "date_naissance": date_naissance.isoformat(),
                    "nationalite": str(row['nationalite']),
                    "localite": str(row['localite']),
                    "codesp": str(row['codesp']),
                    "sp": str(row['sp']),
                    "pere": str(row.get('pere', '')) if pd.notna(row.get('pere')) else None,
                    "mere": str(row.get('mere', '')) if pd.notna(row.get('mere')) else None,
                    "nacte": str(row.get('nacte', '')) if pd.notna(row.get('nacte')) else None,
                    "lieuacte": str(row.get('lieuacte', '')) if pd.notna(row.get('lieuacte')) else None,
                    "residence": str(row.get('residence', '')) if pd.notna(row.get('residence')) else None,
                    "niveau": str(row['niveau']),
                    "statut": "officiel",
                    "photo_url": None,
                    "numero_table": None,
                    "centre_composition": None,
                    "salle": None,
                    "annee_scolaire": annee_scolaire,
                    "date_import": datetime.utcnow().isoformat()
                }
                
                # Vérifier si le candidat existe déjà (par matricule)
                existing = await db.candidats_cepe.find_one({
                    "matricule": candidat["matricule"],
                    "annee_scolaire": annee_scolaire
                })
                
                if existing:
                    # Mettre à jour
                    await db.candidats_cepe.update_one(
                        {"_id": existing["_id"]},
                        {"$set": candidat}
                    )
                else:
                    # Insérer
                    await db.candidats_cepe.insert_one(candidat)
                
                candidats_importes.append(candidat["matricule"])
                
            except Exception as e:
                candidats_erreurs.append({
                    "ligne": index + 2,  # +2 car index commence à 0 et ligne 1 est l'en-tête
                    "matricule": str(row.get('matricule', 'INCONNU')),
                    "erreur": str(e)
                })
        
        return {
            "message": "Importation terminée",
            "candidats_importes": len(candidats_importes),
            "erreurs": len(candidats_erreurs),
            "details_erreurs": candidats_erreurs[:10] if candidats_erreurs else []  # Max 10 erreurs affichées
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'importation: {str(e)}"
        )

@router.post("/photos/zip")
async def import_photos_zip(
    file: UploadFile = File(...),
    ecole: str = Form(...),
    email: str = Depends(verify_email)
):
    """Importer les photos des candidats depuis un fichier ZIP"""
    db = get_db()
    
    if not file.filename.endswith('.zip'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le fichier doit être un fichier ZIP"
        )
    
    try:
        # Lire le contenu du ZIP
        contents = await file.read()
        
        photos_importees = []
        photos_erreurs = []
        
        # Ouvrir le ZIP
        with zipfile.ZipFile(io.BytesIO(contents)) as zip_file:
            # Parcourir tous les fichiers du ZIP
            for file_info in zip_file.filelist:
                filename = file_info.filename
                
                # Ignorer les dossiers et fichiers cachés
                if filename.endswith('/') or filename.startswith('__MACOSX') or '/.DS_Store' in filename:
                    continue
                
                # Vérifier que c'est une image
                if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                
                try:
                    # Extraire le matricule du nom de fichier (sans extension)
                    base_filename = os.path.basename(filename)
                    matricule = os.path.splitext(base_filename)[0]
                    
                    # Chercher le candidat correspondant
                    candidat = await db.candidats_cepe.find_one({
                        "matricule": matricule,
                        "ecole": ecole
                    })
                    
                    if not candidat:
                        photos_erreurs.append({
                            "fichier": filename,
                            "matricule": matricule,
                            "erreur": "Candidat non trouvé"
                        })
                        continue
                    
                    # Extraire et sauvegarder la photo
                    photo_data = zip_file.read(filename)
                    
                    # Créer le chemin de destination
                    extension = os.path.splitext(filename)[1]
                    photo_filename = f"{matricule}{extension}"
                    photo_path = UPLOAD_DIR / photo_filename
                    
                    # Sauvegarder la photo
                    with open(photo_path, 'wb') as f:
                        f.write(photo_data)
                    
                    # Mettre à jour le candidat avec l'URL de la photo
                    photo_url = f"/uploads/photos/{photo_filename}"
                    await db.candidats_cepe.update_one(
                        {"_id": candidat["_id"]},
                        {"$set": {"photo_url": photo_url}}
                    )
                    
                    photos_importees.append({
                        "matricule": matricule,
                        "photo_url": photo_url
                    })
                    
                except Exception as e:
                    photos_erreurs.append({
                        "fichier": filename,
                        "erreur": str(e)
                    })
        
        return {
            "message": "Importation des photos terminée",
            "photos_importees": len(photos_importees),
            "erreurs": len(photos_erreurs),
            "details_erreurs": photos_erreurs[:10] if photos_erreurs else []
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'importation des photos: {str(e)}"
        )

@router.get("/candidats/stats")
async def get_import_stats(annee_scolaire: str, email: str = Depends(verify_email)):
    """Obtenir les statistiques des candidats importés"""
    db = get_db()
    
    total_candidats = await db.candidats_cepe.count_documents({"annee_scolaire": annee_scolaire})
    candidats_avec_photo = await db.candidats_cepe.count_documents({
        "annee_scolaire": annee_scolaire,
        "photo_url": {"$ne": None}
    })
    
    # Statistiques par école
    pipeline = [
        {"$match": {"annee_scolaire": annee_scolaire}},
        {"$group": {
            "_id": "$ecole",
            "total": {"$sum": 1},
            "avec_photo": {
                "$sum": {"$cond": [{"$ne": ["$photo_url", None]}, 1, 0]}
            }
        }},
        {"$sort": {"_id": 1}}
    ]
    
    ecoles_stats = await db.candidats_cepe.aggregate(pipeline).to_list(1000)
    
    return {
        "total_candidats": total_candidats,
        "candidats_avec_photo": candidats_avec_photo,
        "candidats_sans_photo": total_candidats - candidats_avec_photo,
        "taux_photos": round((candidats_avec_photo / total_candidats * 100) if total_candidats > 0 else 0, 2),
        "par_ecole": ecoles_stats
    }

@router.post("/epuration/doublons")
async def epurer_doublons(
    mode: str = "automatique",  # "automatique" ou "manuel"
    matricules_a_supprimer: Optional[List[str]] = None,
    annee_scolaire: str = Form(...),
    email: str = Depends(verify_email)
):
    """Détecter et supprimer les doublons"""
    db = get_db()
    
    # Détecter les doublons
    pipeline = [
        {"$match": {"annee_scolaire": annee_scolaire}},
        {"$group": {
            "_id": "$matricule",
            "count": {"$sum": 1},
            "ids": {"$push": "$id"},
            "noms": {"$push": "$nom"},
            "prenoms": {"$push": "$prenoms"}
        }},
        {"$match": {"count": {"$gt": 1}}}
    ]
    
    doublons = await db.candidats_cepe.aggregate(pipeline).to_list(1000)
    
    if not doublons:
        return {
            "message": "Aucun doublon détecté",
            "doublons_trouves": 0,
            "doublons_supprimes": 0
        }
    
    if mode == "manuel":
        # Mode manuel : retourner la liste des doublons pour validation
        doublons_info = []
        for doublon in doublons:
            doublons_info.append({
                "matricule": doublon["_id"],
                "occurrences": doublon["count"],
                "candidats_ids": doublon["ids"],
                "noms": doublon["noms"][0],
                "prenoms": doublon["prenoms"][0]
            })
        
        return {
            "mode": "manuel",
            "message": "Doublons détectés. Veuillez sélectionner les candidats à supprimer.",
            "doublons": doublons_info
        }
    
    else:  # Mode automatique
        doublons_supprimes = 0
        
        for doublon in doublons:
            # Garder le premier, supprimer les autres
            ids_a_supprimer = doublon["ids"][1:]
            
            for candidat_id in ids_a_supprimer:
                result = await db.candidats_cepe.delete_one({"id": candidat_id})
                if result.deleted_count > 0:
                    doublons_supprimes += 1
        
        return {
            "mode": "automatique",
            "message": "Épuration automatique terminée",
            "doublons_trouves": len(doublons),
            "doublons_supprimes": doublons_supprimes
        }
