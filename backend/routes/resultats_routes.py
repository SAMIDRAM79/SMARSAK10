from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

router = APIRouter(prefix="/resultats", tags=["resultats"])

@router.post("/composition")
async def saisir_resultats_composition(
    candidat_id: str,
    type_examen: str,  # "composition", "examen_blanc", "cepe", "entree_sixieme"
    notes: dict,  # {"matiere": note, ...}
    note_eps: Optional[float] = None,
    annee_scolaire: str = None,
    email: str = Depends(verify_email)
):
    """Saisir les résultats d'une composition pour un candidat"""
    db = get_db()
    
    # Récupérer le candidat
    candidat = await db.candidats_cepe.find_one({"id": candidat_id}, {"_id": 0})
    if not candidat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidat non trouvé"
        )
    
    # Calculer la moyenne
    total_notes = sum(notes.values())
    nb_matieres = len(notes)
    
    # Ajouter EPS uniquement pour examens blancs
    if type_examen == "examen_blanc" and note_eps is not None:
        total_notes += note_eps
        nb_matieres += 1
    
    moyenne = round(total_notes / nb_matieres, 2) if nb_matieres > 0 else 0
    
    # Déterminer la mention
    if moyenne >= 16:
        mention = "Très Bien"
    elif moyenne >= 14:
        mention = "Bien"
    elif moyenne >= 12:
        mention = "Assez Bien"
    elif moyenne >= 10:
        mention = "Passable"
    else:
        mention = "Ajourné"
    
    # Créer le document résultat
    resultat = {
        "id": str(uuid4()),
        "candidat_id": candidat_id,
        "matricule": candidat["matricule"],
        "nom": candidat["nom"],
        "prenoms": candidat["prenoms"],
        "ecole": candidat["ecole"],
        "type_examen": type_examen,
        "notes": notes,
        "note_eps": note_eps,
        "moyenne": moyenne,
        "mention": mention,
        "admis": moyenne >= 10,
        "annee_scolaire": annee_scolaire or candidat["annee_scolaire"],
        "date_saisie": datetime.utcnow().isoformat()
    }
    
    # Vérifier si résultat existe déjà
    existing = await db.resultats_compositions.find_one({
        "candidat_id": candidat_id,
        "type_examen": type_examen,
        "annee_scolaire": resultat["annee_scolaire"]
    })
    
    if existing:
        await db.resultats_compositions.update_one(
            {"_id": existing["_id"]},
            {"$set": resultat}
        )
    else:
        await db.resultats_compositions.insert_one(resultat)
    
    return {
        "message": "Résultats enregistrés avec succès",
        "resultat": resultat
    }

@router.get("/statistiques/ecole/{ecole}")
async def get_stats_ecole(
    ecole: str,
    type_examen: Optional[str] = None,
    annee_scolaire: Optional[str] = None,
    email: str = Depends(verify_email)
):
    """Statistiques des résultats par école"""
    db = get_db()
    
    query = {"ecole": ecole}
    if type_examen:
        query["type_examen"] = type_examen
    if annee_scolaire:
        query["annee_scolaire"] = annee_scolaire
    
    resultats = await db.resultats_compositions.find(query, {"_id": 0}).to_list(10000)
    
    if not resultats:
        return {
            "ecole": ecole,
            "total_candidats": 0,
            "admis": 0,
            "ajournes": 0,
            "taux_reussite": 0,
            "moyenne_generale": 0
        }
    
    total = len(resultats)
    admis = sum(1 for r in resultats if r["admis"])
    moyennes = [r["moyenne"] for r in resultats]
    
    return {
        "ecole": ecole,
        "total_candidats": total,
        "admis": admis,
        "ajournes": total - admis,
        "taux_reussite": round((admis / total * 100), 2) if total > 0 else 0,
        "moyenne_generale": round(sum(moyennes) / len(moyennes), 2) if moyennes else 0,
        "mentions": {
            "tres_bien": sum(1 for r in resultats if r["mention"] == "Très Bien"),
            "bien": sum(1 for r in resultats if r["mention"] == "Bien"),
            "assez_bien": sum(1 for r in resultats if r["mention"] == "Assez Bien"),
            "passable": sum(1 for r in resultats if r["mention"] == "Passable")
        }
    }

@router.get("/statistiques/secteur/{secteur}")
async def get_stats_secteur(
    secteur: str,
    type_examen: Optional[str] = None,
    annee_scolaire: Optional[str] = None,
    email: str = Depends(verify_email)
):
    """Statistiques des résultats par secteur pédagogique"""
    db = get_db()
    
    # Récupérer le secteur
    secteur_doc = await db.secteurs_pedagogiques.find_one({"nom": secteur})
    if not secteur_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Secteur non trouvé"
        )
    
    ecoles = secteur_doc.get("ecoles", [])
    
    query = {"ecole": {"$in": ecoles}}
    if type_examen:
        query["type_examen"] = type_examen
    if annee_scolaire:
        query["annee_scolaire"] = annee_scolaire
    
    resultats = await db.resultats_compositions.find(query, {"_id": 0}).to_list(10000)
    
    if not resultats:
        return {
            "secteur": secteur,
            "total_candidats": 0,
            "admis": 0,
            "taux_reussite": 0
        }
    
    total = len(resultats)
    admis = sum(1 for r in resultats if r["admis"])
    moyennes = [r["moyenne"] for r in resultats]
    
    # Stats par école du secteur
    stats_ecoles = {}
    for ecole in ecoles:
        ecole_resultats = [r for r in resultats if r["ecole"] == ecole]
        if ecole_resultats:
            ecole_total = len(ecole_resultats)
            ecole_admis = sum(1 for r in ecole_resultats if r["admis"])
            stats_ecoles[ecole] = {
                "total": ecole_total,
                "admis": ecole_admis,
                "taux_reussite": round((ecole_admis / ecole_total * 100), 2)
            }
    
    return {
        "secteur": secteur,
        "total_candidats": total,
        "admis": admis,
        "ajournes": total - admis,
        "taux_reussite": round((admis / total * 100), 2) if total > 0 else 0,
        "moyenne_generale": round(sum(moyennes) / len(moyennes), 2) if moyennes else 0,
        "stats_par_ecole": stats_ecoles
    }

@router.get("/statistiques/commune/{commune}")
async def get_stats_commune(
    commune: str,
    type_examen: Optional[str] = None,
    annee_scolaire: Optional[str] = None,
    email: str = Depends(verify_email)
):
    """Statistiques des résultats par commune"""
    db = get_db()
    
    # Trouver tous les candidats de cette commune (via localité ou résidence)
    candidats_commune = await db.candidats_cepe.find(
        {"$or": [{"localite": commune}, {"residence": commune}]},
        {"_id": 0, "id": 1}
    ).to_list(10000)
    
    candidats_ids = [c["id"] for c in candidats_commune]
    
    query = {"candidat_id": {"$in": candidats_ids}}
    if type_examen:
        query["type_examen"] = type_examen
    if annee_scolaire:
        query["annee_scolaire"] = annee_scolaire
    
    resultats = await db.resultats_compositions.find(query, {"_id": 0}).to_list(10000)
    
    if not resultats:
        return {
            "commune": commune,
            "total_candidats": 0,
            "admis": 0,
            "taux_reussite": 0
        }
    
    total = len(resultats)
    admis = sum(1 for r in resultats if r["admis"])
    moyennes = [r["moyenne"] for r in resultats]
    
    return {
        "commune": commune,
        "total_candidats": total,
        "admis": admis,
        "ajournes": total - admis,
        "taux_reussite": round((admis / total * 100), 2) if total > 0 else 0,
        "moyenne_generale": round(sum(moyennes) / len(moyennes), 2) if moyennes else 0
    }

@router.get("/statistiques/sous-prefecture/{sp}")
async def get_stats_sous_prefecture(
    sp: str,
    type_examen: Optional[str] = None,
    annee_scolaire: Optional[str] = None,
    email: str = Depends(verify_email)
):
    """Statistiques des résultats par sous-préfecture"""
    db = get_db()
    
    # Trouver tous les candidats de cette sous-préfecture
    candidats_sp = await db.candidats_cepe.find(
        {"sp": sp},
        {"_id": 0, "id": 1}
    ).to_list(10000)
    
    candidats_ids = [c["id"] for c in candidats_sp]
    
    query = {"candidat_id": {"$in": candidats_ids}}
    if type_examen:
        query["type_examen"] = type_examen
    if annee_scolaire:
        query["annee_scolaire"] = annee_scolaire
    
    resultats = await db.resultats_compositions.find(query, {"_id": 0}).to_list(10000)
    
    if not resultats:
        return {
            "sous_prefecture": sp,
            "total_candidats": 0,
            "admis": 0,
            "taux_reussite": 0
        }
    
    total = len(resultats)
    admis = sum(1 for r in resultats if r["admis"])
    moyennes = [r["moyenne"] for r in resultats]
    
    return {
        "sous_prefecture": sp,
        "total_candidats": total,
        "admis": admis,
        "ajournes": total - admis,
        "taux_reussite": round((admis / total * 100), 2) if total > 0 else 0,
        "moyenne_generale": round(sum(moyennes) / len(moyennes), 2) if moyennes else 0
    }
