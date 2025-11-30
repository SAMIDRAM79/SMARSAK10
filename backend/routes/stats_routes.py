from fastapi import APIRouter, Depends
from database import get_db
from auth_middleware import verify_email
from bson import ObjectId

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/dashboard")
async def get_dashboard_stats(email: str = Depends(verify_email)):
    """Récupérer les statistiques du tableau de bord"""
    db = get_db()
    annee_scolaire = "2024-2025"
    
    try:
        # Effectifs par niveau
        total_students = await db.students.count_documents({"statut": "actif"})
    total_pre_primaire = await db.students.count_documents({"niveau": "pre_primaire", "statut": "actif"})
    total_maternelle = await db.students.count_documents({"niveau": "maternelle", "statut": "actif"})
    total_primaire = await db.students.count_documents({"niveau": "primaire", "statut": "actif"})
    
    # Effectifs par genre
    total_garcons = await db.students.count_documents({"genre": "masculin", "statut": "actif"})
    total_filles = await db.students.count_documents({"genre": "feminin", "statut": "actif"})
    
    # Nombre de classes
    total_classes = await db.classes.count_documents({"annee_scolaire": annee_scolaire})
    
    # Nombre d'enseignants
    total_enseignants = await db.enseignants.count_documents({"statut": "actif"})
    
    # Statistiques financières
    pipeline_recettes = [
        {"$group": {"_id": None, "total": {"$sum": "$montant"}}}
    ]
    frais_result = await db.frais.aggregate(pipeline_recettes).to_list(1)
    total_frais = frais_result[0]["total"] if frais_result else 0
    
    pipeline_paiements = [
        {"$group": {"_id": None, "total": {"$sum": "$montant_paye"}}}
    ]
    paiements_result = await db.paiements.aggregate(pipeline_paiements).to_list(1)
    total_paiements = paiements_result[0]["total"] if paiements_result else 0
    
    taux_paiement = (total_paiements / (total_frais * total_students) * 100) if (total_frais * total_students) > 0 else 0
    
    # Statistiques par classe
    classes = await db.classes.find({"annee_scolaire": annee_scolaire}).to_list(100)
    stats_classes = []
    
    for classe in classes:
        effectif = await db.students.count_documents({
            "classe": classe["nom"],
            "statut": "actif"
        })
        garcons = await db.students.count_documents({
            "classe": classe["nom"],
            "statut": "actif",
            "genre": "masculin"
        })
        filles = await db.students.count_documents({
            "classe": classe["nom"],
            "statut": "actif",
            "genre": "feminin"
        })
        
        stats_classes.append({
            "classe": classe["nom"],
            "niveau": classe["niveau"],
            "effectif": effectif,
            "garcons": garcons,
            "filles": filles
        })
    
    return {
        "effectifs": {
            "total": total_students,
            "pre_primaire": total_pre_primaire,
            "maternelle": total_maternelle,
            "primaire": total_primaire,
            "garcons": total_garcons,
            "filles": total_filles
        },
        "classes": {
            "total": total_classes,
            "details": stats_classes
        },
        "personnel": {
            "enseignants": total_enseignants
        },
        "finances": {
            "total_frais_annee": round(total_frais * total_students, 2),
            "total_paiements": round(total_paiements, 2),
            "taux_paiement": round(taux_paiement, 2)
        },
        "annee_scolaire": annee_scolaire
    }
    except Exception as e:
        # Return empty stats if database is not accessible yet
        return {
            "effectifs": {
                "total": 0,
                "pre_primaire": 0,
                "maternelle": 0,
                "primaire": 0,
                "garcons": 0,
                "filles": 0
            },
            "classes": {
                "total": 0,
                "details": []
            },
            "personnel": {
                "enseignants": 0
            },
            "finances": {
                "total_frais_annee": 0,
                "total_paiements": 0,
                "taux_paiement": 0
            },
            "annee_scolaire": annee_scolaire,
            "error": "Database not ready or not accessible"
        }

@router.get("/classe/{classe_nom}")
async def get_classe_stats(classe_nom: str, email: str = Depends(verify_email)):
    """Statistiques détaillées d'une classe"""
    db = get_db()
    
    # Effectif
    effectif_total = await db.students.count_documents({
        "classe": classe_nom,
        "statut": "actif"
    })
    effectif_garcons = await db.students.count_documents({
        "classe": classe_nom,
        "statut": "actif",
        "genre": "masculin"
    })
    effectif_filles = await db.students.count_documents({
        "classe": classe_nom,
        "statut": "actif",
        "genre": "feminin"
    })
    
    # Récupérer les bulletins de la classe
    students = await db.students.find({
        "classe": classe_nom,
        "statut": "actif"
    }).to_list(1000)
    
    student_ids = [str(s["_id"]) for s in students]
    bulletins = await db.bulletins.find({
        "student_id": {"$in": student_ids},
        "periode": "trimestre_1"  # Dernière période
    }).to_list(1000)
    
    moyennes = [b["moyenne_generale"] for b in bulletins]
    moyenne_classe = sum(moyennes) / len(moyennes) if moyennes else 0
    
    # Taux de réussite (>= 10/20)
    reussis = sum(1 for m in moyennes if m >= 10)
    taux_reussite = (reussis / len(moyennes) * 100) if moyennes else 0
    
    return {
        "classe": classe_nom,
        "effectif_total": effectif_total,
        "effectif_garcons": effectif_garcons,
        "effectif_filles": effectif_filles,
        "moyenne_classe": round(moyenne_classe, 2),
        "taux_reussite": round(taux_reussite, 2)
    }
