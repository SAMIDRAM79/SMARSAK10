"""
Script pour créer les index MongoDB pour optimiser les performances
"""
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'smartscool')

async def create_indexes():
    """Créer tous les index nécessaires"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("Création des index MongoDB...")
    
    # Index pour students
    await db.students.create_index("matricule")
    await db.students.create_index([("classe", 1), ("statut", 1)])
    await db.students.create_index([("niveau", 1), ("statut", 1)])
    print("✅ Index students créés")
    
    # Index pour candidats_cepe
    await db.candidats_cepe.create_index([("matricule", 1), ("annee_scolaire", 1)], unique=True)
    await db.candidats_cepe.create_index("ecole")
    await db.candidats_cepe.create_index("niveau")
    await db.candidats_cepe.create_index([("nom", 1), ("prenoms", 1)])
    print("✅ Index candidats_cepe créés")
    
    # Index pour notes
    await db.notes.create_index([("student_id", 1), ("periode", 1)])
    await db.notes.create_index("matiere_id")
    print("✅ Index notes créés")
    
    # Index pour bulletins
    await db.bulletins.create_index([("student_id", 1), ("periode", 1), ("annee_scolaire", 1)])
    print("✅ Index bulletins créés")
    
    # Index pour resultats_compositions
    await db.resultats_compositions.create_index([("candidat_id", 1), ("type_examen", 1)])
    await db.resultats_compositions.create_index("ecole")
    await db.resultats_compositions.create_index("annee_scolaire")
    print("✅ Index resultats_compositions créés")
    
    # Index pour centres_composition
    await db.centres_composition.create_index("annee_scolaire")
    print("✅ Index centres_composition créés")
    
    # Index pour secteurs_pedagogiques
    await db.secteurs_pedagogiques.create_index([("nom", 1), ("annee_scolaire", 1)])
    print("✅ Index secteurs_pedagogiques créés")
    
    print("\n✅ Tous les index ont été créés avec succès !")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_indexes())
