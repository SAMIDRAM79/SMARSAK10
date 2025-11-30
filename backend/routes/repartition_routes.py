from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import List
from bson import ObjectId
import math

router = APIRouter(prefix="/repartition", tags=["repartition"])

# Règles de répartition
RATIO_CANDIDATS_PAR_SALLE = 28
MAX_SALLES_PAR_CENTRE = 16
MAX_CANDIDATS_PAR_CENTRE = 480
SALLES_29_30_AUTORISEES = True  # Pour IEPP avec effectifs > 28

@router.get("/centres")
async def get_centres_composition(email: str = Depends(verify_email)):
    """Récupérer tous les centres de composition"""
    db = get_db()
    
    centres = await db.centres_composition.find().sort("nom", 1).to_list(1000)
    return [serialize_doc(centre) for centre in centres]

@router.post("/centres")
async def create_centre_composition(nom: str, capacite_max: int = MAX_CANDIDATS_PAR_CENTRE, email: str = Depends(verify_email)):
    """Créer un nouveau centre de composition"""
    db = get_db()
    
    centre_dict = {
        "nom": nom,
        "capacite_max": capacite_max,
        "nb_salles": 0,
        "nb_candidats": 0,
        "ecoles_affectees": []
    }
    
    result = await db.centres_composition.insert_one(centre_dict)
    return {
        "id": str(result.inserted_id),
        "message": "Centre de composition créé avec succès"
    }

@router.post("/calculer")
async def calculer_repartition(email: str = Depends(verify_email)):
    """Calculer automatiquement la répartition des écoles dans les centres"""
    db = get_db()
    
    # Récupérer tous les élèves actifs (candidats)
    candidats = await db.students.find({"statut": "actif"}).to_list(10000)
    
    # Grouper par école (classe)
    ecoles = {}
    for candidat in candidats:
        classe = candidat.get("classe", "Inconnu")
        if classe not in ecoles:
            ecoles[classe] = []
        ecoles[classe].append(candidat)
    
    # Récupérer les centres disponibles
    centres = await db.centres_composition.find().sort("nom", 1).to_list(1000)
    
    if not centres:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucun centre de composition disponible. Veuillez d'abord créer des centres."
        )
    
    repartition = []
    centre_index = 0
    candidats_dans_centre_actuel = 0
    salles_dans_centre_actuel = 0
    
    for ecole, eleves in ecoles.items():
        nb_candidats = len(eleves)
        
        # Calculer le nombre de salles nécessaires pour cette école
        if SALLES_29_30_AUTORISEES and nb_candidats > RATIO_CANDIDATS_PAR_SALLE:
            # Autoriser 29-30 candidats par salle
            nb_salles = math.ceil(nb_candidats / 30)
        else:
            # Ratio standard de 28
            nb_salles = math.ceil(nb_candidats / RATIO_CANDIDATS_PAR_SALLE)
        
        # Vérifier si l'école peut tenir dans le centre actuel
        if (candidats_dans_centre_actuel + nb_candidats > MAX_CANDIDATS_PAR_CENTRE or 
            salles_dans_centre_actuel + nb_salles > MAX_SALLES_PAR_CENTRE):
            # Passer au centre suivant
            centre_index += 1
            if centre_index >= len(centres):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Pas assez de centres de composition pour tous les candidats. Créez plus de centres."
                )
            candidats_dans_centre_actuel = 0
            salles_dans_centre_actuel = 0
        
        # Affecter l'école au centre
        centre = centres[centre_index]
        candidats_dans_centre_actuel += nb_candidats
        salles_dans_centre_actuel += nb_salles
        
        # Calculer la répartition des candidats par salle
        salles_detail = []
        candidats_restants = nb_candidats
        for i in range(nb_salles):
            if i == nb_salles - 1:
                # Dernière salle : prendre tous les candidats restants
                nb_dans_salle = candidats_restants
            else:
                # Salles normales
                if SALLES_29_30_AUTORISEES and nb_candidats > RATIO_CANDIDATS_PAR_SALLE:
                    nb_dans_salle = min(30, candidats_restants)
                else:
                    nb_dans_salle = min(RATIO_CANDIDATS_PAR_SALLE, candidats_restants)
            
            salles_detail.append({
                "numero_salle": i + 1,
                "nb_candidats": nb_dans_salle
            })
            candidats_restants -= nb_dans_salle
        
        repartition.append({
            "ecole": ecole,
            "centre": centre["nom"],
            "centre_id": str(centre["_id"]),
            "nb_candidats": nb_candidats,
            "nb_salles": nb_salles,
            "salles": salles_detail
        })
    
    # Mettre à jour la base de données
    await db.repartitions.delete_many({})  # Supprimer anciennes répartitions
    if repartition:
        await db.repartitions.insert_many(repartition)
    
    return {
        "message": "Répartition calculée avec succès",
        "total_ecoles": len(repartition),
        "total_candidats": sum(r["nb_candidats"] for r in repartition),
        "centres_utilises": len(set(r["centre"] for r in repartition)),
        "repartition": repartition
    }

@router.get("/repartition")
async def get_repartition(email: str = Depends(verify_email)):
    """Récupérer la répartition actuelle"""
    db = get_db()
    
    repartition = await db.repartitions.find().to_list(1000)
    return [serialize_doc(r) for r in repartition]

@router.get("/export")
async def export_repartition(email: str = Depends(verify_email)):
    """Exporter la répartition au format CSV"""
    db = get_db()
    
    repartition = await db.repartitions.find().to_list(1000)
    
    if not repartition:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucune répartition disponible. Calculez d'abord la répartition."
        )
    
    # Créer le CSV
    csv_lines = ["École,Centre,Nombre de candidats,Nombre de salles,Détail des salles"]
    
    for r in repartition:
        salles_str = " | ".join([f"Salle {s['numero_salle']}: {s['nb_candidats']} candidats" for s in r["salles"]])
        csv_lines.append(f"{r['ecole']},{r['centre']},{r['nb_candidats']},{r['nb_salles']},\"{salles_str}\"")
    
    return {
        "csv": "\n".join(csv_lines),
        "filename": "repartition_centres_composition.csv"
    }

@router.post("/verifier-doublons")
async def verifier_doublons(email: str = Depends(verify_email)):
    """Vérifier et supprimer les doublons dans les élèves"""
    db = get_db()
    
    # Trouver les doublons par matricule
    pipeline = [
        {"$group": {
            "_id": "$matricule",
            "count": {"$sum": 1},
            "ids": {"$push": "$_id"}
        }},
        {"$match": {"count": {"$gt": 1}}}
    ]
    
    doublons = await db.students.aggregate(pipeline).to_list(1000)
    
    doublons_supprimes = 0
    for doublon in doublons:
        # Garder le premier, supprimer les autres
        ids_a_supprimer = doublon["ids"][1:]
        for id_to_delete in ids_a_supprimer:
            await db.students.delete_one({"_id": id_to_delete})
            doublons_supprimes += 1
    
    return {
        "message": "Vérification terminée",
        "doublons_trouves": len(doublons),
        "doublons_supprimes": doublons_supprimes
    }
