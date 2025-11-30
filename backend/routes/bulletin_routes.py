from fastapi import APIRouter, HTTPException, status, Depends
from models import Bulletin, BulletinCreate
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import List
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/bulletins", tags=["bulletins"])

async def calculer_moyenne_eleve(student_id: str, periode: str, annee_scolaire: str, db):
    """Calculer la moyenne générale d'un élève"""
    # Récupérer toutes les notes de l'élève pour la période
    notes = await db.notes.find({
        "student_id": student_id,
        "periode": periode,
        "annee_scolaire": annee_scolaire
    }).to_list(1000)
    
    if not notes:
        return 0, []
    
    # Regrouper les notes par matière et prendre la dernière
    notes_par_matiere = {}
    for note in notes:
        matiere_id = note["matiere_id"]
        if matiere_id not in notes_par_matiere or note["date_saisie"] > notes_par_matiere[matiere_id]["date_saisie"]:
            notes_par_matiere[matiere_id] = note
    
    # Calculer la moyenne avec coefficients
    total_points = 0
    total_coefficients = 0
    notes_detail = []
    
    for matiere_id, note in notes_par_matiere.items():
        matiere = await db.matieres.find_one({"_id": ObjectId(matiere_id)})
        if matiere:
            # Convertir la note sur 20
            note_sur_20 = (note["note"] / note["note_sur"]) * 20
            coefficient = matiere.get("coefficient", 1.0)
            
            total_points += note_sur_20 * coefficient
            total_coefficients += coefficient
            
            notes_detail.append({
                "matiere": matiere["nom"],
                "note": note["note"],
                "note_sur": note["note_sur"],
                "note_sur_20": round(note_sur_20, 2),
                "coefficient": coefficient,
                "type_examen": note["type_examen"]
            })
    
    moyenne = total_points / total_coefficients if total_coefficients > 0 else 0
    return round(moyenne, 2), notes_detail

@router.post("/generate", response_model=dict)
async def generate_bulletin(
    student_id: str,
    periode: str,
    annee_scolaire: str,
    email: str = Depends(verify_email)
):
    """Générer un bulletin pour un élève"""
    db = get_db()
    
    # Récupérer l'élève
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Élève non trouvé"
        )
    
    # Calculer la moyenne
    moyenne, notes_detail = await calculer_moyenne_eleve(student_id, periode, annee_scolaire, db)
    
    if not notes_detail:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucune note trouvée pour cette période"
        )
    
    # Déterminer l'appréciation
    if moyenne >= 16:
        appreciation = "Excellent"
    elif moyenne >= 14:
        appreciation = "Très bien"
    elif moyenne >= 12:
        appreciation = "Bien"
    elif moyenne >= 10:
        appreciation = "Assez bien"
    else:
        appreciation = "Passable"
    
    # Calculer le rang dans la classe
    students_classe = await db.students.find({
        "classe": student["classe"],
        "statut": "actif"
    }).to_list(1000)
    
    moyennes_classe = []
    for s in students_classe:
        moy, _ = await calculer_moyenne_eleve(str(s["_id"]), periode, annee_scolaire, db)
        moyennes_classe.append((str(s["_id"]), moy))
    
    moyennes_classe.sort(key=lambda x: x[1], reverse=True)
    rang = next((i + 1 for i, (sid, _) in enumerate(moyennes_classe) if sid == student_id), None)
    
    # Créer le bulletin
    bulletin_dict = {
        "student_id": student_id,
        "classe": student["classe"],
        "periode": periode,
        "annee_scolaire": annee_scolaire,
        "notes": notes_detail,
        "moyenne_generale": moyenne,
        "rang": rang,
        "appreciation": appreciation,
        "date_generation": datetime.utcnow()
    }
    
    # Vérifier si un bulletin existe déjà
    existing = await db.bulletins.find_one({
        "student_id": student_id,
        "periode": periode,
        "annee_scolaire": annee_scolaire
    })
    
    if existing:
        # Mettre à jour
        await db.bulletins.update_one(
            {"_id": existing["_id"]},
            {"$set": bulletin_dict}
        )
        bulletin_id = str(existing["_id"])
    else:
        # Créer
        result = await db.bulletins.insert_one(bulletin_dict)
        bulletin_id = str(result.inserted_id)
    
    return {
        "id": bulletin_id,
        "moyenne": moyenne,
        "rang": rang,
        "appreciation": appreciation,
        "message": "Bulletin généré avec succès"
    }

@router.get("/student/{student_id}", response_model=List[dict])
async def get_student_bulletins(student_id: str, email: str = Depends(verify_email)):
    """Récupérer les bulletins d'un élève"""
    db = get_db()
    
    bulletins = await db.bulletins.find({"student_id": student_id}).sort("date_generation", -1).to_list(100)
    return [serialize_doc(bulletin) for bulletin in bulletins]

@router.get("/{bulletin_id}", response_model=dict)
async def get_bulletin(bulletin_id: str, email: str = Depends(verify_email)):
    """Récupérer un bulletin par son ID"""
    db = get_db()
    
    try:
        bulletin = await db.bulletins.find_one({"_id": ObjectId(bulletin_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID invalide"
        )
    
    if not bulletin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bulletin non trouvé"
        )
    
    # Enrichir avec les infos de l'élève
    bulletin_doc = serialize_doc(bulletin)
    student = await db.students.find_one({"_id": ObjectId(bulletin["student_id"])})
    if student:
        bulletin_doc["student"] = serialize_doc(student)
    
    return bulletin_doc
