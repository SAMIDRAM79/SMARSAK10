"""
Script d'initialisation de la base de données SMARTSAK10
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def seed_database():
    # Connexion MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'smartscool')]
    
    print("🌱 Initialisation de SMARTSAK10...")
    
    # Nettoyer les anciennes collections
    await db.students.delete_many({})
    await db.classes.delete_many({})
    await db.matieres.delete_many({})
    await db.enseignants.delete_many({})
    await db.notes.delete_many({})
    await db.bulletins.delete_many({})
    
    # 1. Créer les classes
    classes_data = [
        # Pré-primaire
        {"nom": "PS1", "niveau": "pre_primaire", "effectif_max": 30, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
        {"nom": "PS2", "niveau": "pre_primaire", "effectif_max": 30, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
        
        # Maternelle
        {"nom": "MS1", "niveau": "maternelle", "effectif_max": 35, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
        {"nom": "MS2", "niveau": "maternelle", "effectif_max": 35, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
        {"nom": "GS1", "niveau": "maternelle", "effectif_max": 35, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
        {"nom": "GS2", "niveau": "maternelle", "effectif_max": 35, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
        
        # Primaire
        {"nom": "CP1", "niveau": "primaire", "effectif_max": 40, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
        {"nom": "CP2", "niveau": "primaire", "effectif_max": 40, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
        {"nom": "CE1", "niveau": "primaire", "effectif_max": 40, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
        {"nom": "CE2", "niveau": "primaire", "effectif_max": 40, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
        {"nom": "CM1", "niveau": "primaire", "effectif_max": 40, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
        {"nom": "CM2", "niveau": "primaire", "effectif_max": 40, "annee_scolaire": "2024-2025", "effectif_actuel": 0},
    ]
    
    result = await db.classes.insert_many(classes_data)
    print(f"✅ {len(result.inserted_ids)} classes créées")
    
    # 2. Créer les matières
    matieres_data = [
        # Matières primaire
        {"nom": "Exploitation de texte", "note_sur": 50, "niveau": "primaire", "coefficient": 2.0},
        {"nom": "Éveil au milieu", "note_sur": 50, "niveau": "primaire", "coefficient": 2.0},
        {"nom": "Dictée", "note_sur": 20, "niveau": "primaire", "coefficient": 1.0},
        {"nom": "Mathématiques", "note_sur": 50, "niveau": "primaire", "coefficient": 2.0},
        {"nom": "EPS", "note_sur": 20, "niveau": "primaire", "coefficient": 1.0},
        
        # Matières maternelle (adaptées)
        {"nom": "Langage", "note_sur": 50, "niveau": "maternelle", "coefficient": 2.0},
        {"nom": "Découverte du monde", "note_sur": 50, "niveau": "maternelle", "coefficient": 2.0},
        {"nom": "Activités artistiques", "note_sur": 20, "niveau": "maternelle", "coefficient": 1.0},
        {"nom": "Mathématiques", "note_sur": 50, "niveau": "maternelle", "coefficient": 2.0},
        {"nom": "EPS", "note_sur": 20, "niveau": "maternelle", "coefficient": 1.0},
        
        # Matières pré-primaire (adaptées)
        {"nom": "Langage oral", "note_sur": 50, "niveau": "pre_primaire", "coefficient": 2.0},
        {"nom": "Découverte", "note_sur": 50, "niveau": "pre_primaire", "coefficient": 2.0},
        {"nom": "Activités manuelles", "note_sur": 20, "niveau": "pre_primaire", "coefficient": 1.0},
        {"nom": "Jeux éducatifs", "note_sur": 50, "niveau": "pre_primaire", "coefficient": 2.0},
        {"nom": "EPS", "note_sur": 20, "niveau": "pre_primaire", "coefficient": 1.0},
    ]
    
    result = await db.matieres.insert_many(matieres_data)
    print(f"✅ {len(result.inserted_ids)} matières créées")
    
    # 3. Créer des enseignants
    enseignants_data = [
        {
            "matricule": "ENS001",
            "nom": "KOUAME",
            "prenoms": "Jean-Baptiste",
            "genre": "masculin",
            "telephone": "0701020304",
            "email": "jb.kouame@smartsak10.edu",
            "specialite": "Français",
            "date_embauche": "2020-09-01",
            "statut": "actif"
        },
        {
            "matricule": "ENS002",
            "nom": "TRAORE",
            "prenoms": "Aminata",
            "genre": "feminin",
            "telephone": "0702030405",
            "email": "a.traore@smartsak10.edu",
            "specialite": "Mathématiques",
            "date_embauche": "2019-09-01",
            "statut": "actif"
        },
        {
            "matricule": "ENS003",
            "nom": "KONE",
            "prenoms": "Moussa",
            "genre": "masculin",
            "telephone": "0703040506",
            "email": "m.kone@smartsak10.edu",
            "specialite": "Sciences",
            "date_embauche": "2021-09-01",
            "statut": "actif"
        },
        {
            "matricule": "ENS004",
            "nom": "YAO",
            "prenoms": "Akissi Marie",
            "genre": "feminin",
            "telephone": "0704050607",
            "email": "am.yao@smartsak10.edu",
            "specialite": "Maternelle",
            "date_embauche": "2018-09-01",
            "statut": "actif"
        }
    ]
    
    result = await db.enseignants.insert_many(enseignants_data)
    print(f"✅ {len(result.inserted_ids)} enseignants créés")
    
    # 4. Créer des élèves de démonstration
    students_data = [
        {
            "matricule": "CP1-2024-001",
            "nom": "DIALLO",
            "prenoms": "Ibrahim",
            "date_naissance": date(2017, 3, 15),
            "lieu_naissance": "Abidjan",
            "genre": "masculin",
            "niveau": "primaire",
            "classe": "CP1",
            "nom_pere": "DIALLO Mamadou",
            "nom_mere": "KONE Fatoumata",
            "telephone_tuteur": "0707080910",
            "adresse": "Cocody, Abidjan",
            "annee_scolaire": "2024-2025",
            "date_inscription": datetime.utcnow(),
            "statut": "actif"
        },
        {
            "matricule": "CP1-2024-002",
            "nom": "KOUASSI",
            "prenoms": "Aya",
            "date_naissance": date(2017, 5, 20),
            "lieu_naissance": "Abidjan",
            "genre": "feminin",
            "niveau": "primaire",
            "classe": "CP1",
            "nom_pere": "KOUASSI Yao",
            "nom_mere": "N'GUESSAN Adjoua",
            "telephone_tuteur": "0708091011",
            "adresse": "Plateau, Abidjan",
            "annee_scolaire": "2024-2025",
            "date_inscription": datetime.utcnow(),
            "statut": "actif"
        },
        {
            "matricule": "CE1-2024-001",
            "nom": "BAMBA",
            "prenoms": "Karim",
            "date_naissance": date(2016, 8, 10),
            "lieu_naissance": "Bouaké",
            "genre": "masculin",
            "niveau": "primaire",
            "classe": "CE1",
            "nom_pere": "BAMBA Seydou",
            "nom_mere": "TOURE Mariam",
            "telephone_tuteur": "0709101112",
            "adresse": "Yopougon, Abidjan",
            "annee_scolaire": "2024-2025",
            "date_inscription": datetime.utcnow(),
            "statut": "actif"
        },
        {
            "matricule": "GS1-2024-001",
            "nom": "OUATTARA",
            "prenoms": "Aminata",
            "date_naissance": date(2019, 2, 14),
            "lieu_naissance": "Abidjan",
            "genre": "feminin",
            "niveau": "maternelle",
            "classe": "GS1",
            "nom_pere": "OUATTARA Dramane",
            "nom_mere": "SANOGO Awa",
            "telephone_tuteur": "0710111213",
            "adresse": "Abobo, Abidjan",
            "annee_scolaire": "2024-2025",
            "date_inscription": datetime.utcnow(),
            "statut": "actif"
        },
        {
            "matricule": "PS1-2024-001",
            "nom": "KOFFI",
            "prenoms": "Marc",
            "date_naissance": date(2021, 6, 5),
            "lieu_naissance": "Abidjan",
            "genre": "masculin",
            "niveau": "pre_primaire",
            "classe": "PS1",
            "nom_pere": "KOFFI Jean",
            "nom_mere": "ASSI Marie",
            "telephone_tuteur": "0711121314",
            "adresse": "Marcory, Abidjan",
            "annee_scolaire": "2024-2025",
            "date_inscription": datetime.utcnow(),
            "statut": "actif"
        }
    ]
    
    result = await db.students.insert_many(students_data)
    print(f"✅ {len(result.inserted_ids)} élèves créés")
    
    # Mettre à jour les effectifs des classes
    for student in students_data:
        await db.classes.update_one(
            {"nom": student["classe"]},
            {"$inc": {"effectif_actuel": 1}}
        )
    
    print("\n✨ Base de données SMARTSAK10 initialisée avec succès!")
    print("\n📊 Résumé:")
    print(f"   - Classes: {len(classes_data)} (Pré-primaire: 2, Maternelle: 4, Primaire: 6)")
    print(f"   - Matières: {len(matieres_data)}")
    print(f"   - Enseignants: {len(enseignants_data)}")
    print(f"   - Élèves: {len(students_data)}")
    print("\n🔑 Accès administrateur: konatdra@gmail.com")
    print("\n🚀 L'application est prête à l'emploi!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
