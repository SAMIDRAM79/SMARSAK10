"""
Seed data script to initialize the database with sample data
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
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'smartscool')]
    
    print("🌱 Seeding database with sample data...")
    
    # Seed Downloads
    downloads_data = [
        {
            "name": "SmartIEPP Kit Complet",
            "version": "v.25.11.25",
            "size": "435 Mo",
            "type": "kit_complet",
            "file_url": "/api/downloads/file/SmartIEPP_Kit_Complet.exe",
            "release_date": datetime(2025, 11, 25),
            "downloads": 0
        },
        {
            "name": "SmartIEPP Mise à jour",
            "version": "v.25.11.25",
            "size": "436 Mo",
            "type": "mise_a_jour",
            "file_url": "/api/downloads/file/SmartIEPP_Update.exe",
            "release_date": datetime(2025, 11, 25),
            "downloads": 0
        },
        {
            "name": "SmartIEPP Ancienne Version",
            "version": "v.24.10.15",
            "size": "420 Mo",
            "type": "ancienne_version",
            "file_url": "/api/downloads/file/SmartIEPP_Old.apk",
            "release_date": datetime(2024, 10, 15),
            "downloads": 0
        }
    ]
    
    # Clear existing downloads
    await db.downloads.delete_many({})
    result = await db.downloads.insert_many(downloads_data)
    print(f"✅ Inserted {len(result.inserted_ids)} downloads")
    
    # Seed Products
    products_data = [
        {
            "name": "SmartIEPP",
            "description": "Logiciel de gestion scolaire complet pour les établissements privés",
            "features": [
                "Gestion des élèves",
                "Notes et bulletins",
                "Comptabilité",
                "Emploi du temps",
                "Gestion du personnel",
                "Rapports statistiques"
            ],
            "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=300&fit=crop",
            "price": 500000,
            "active": True
        },
        {
            "name": "SmartGestion",
            "description": "Solution de gestion d'entreprise adaptée à vos besoins",
            "features": [
                "Facturation automatique",
                "Gestion de stock",
                "Suivi clients",
                "Rapports financiers",
                "Inventaire",
                "Multi-utilisateurs"
            ],
            "image": "https://images.unsplash.com/photo-1575388902449-6bca946ad549?w=400&h=300&fit=crop",
            "price": 350000,
            "active": True
        },
        {
            "name": "SmartCompta",
            "description": "Logiciel de comptabilité moderne et intuitif",
            "features": [
                "Bilan comptable",
                "Journal des opérations",
                "Grand livre",
                "Déclarations fiscales",
                "Plan comptable",
                "Export Excel"
            ],
            "image": "https://images.unsplash.com/photo-1631006732121-a6da2f4864d3?w=400&h=300&fit=crop",
            "price": 250000,
            "active": True
        }
    ]
    
    # Clear existing products
    await db.products.delete_many({})
    result = await db.products.insert_many(products_data)
    print(f"✅ Inserted {len(result.inserted_ids)} products")
    
    print("\n✨ Database seeding completed successfully!")
    print("\n📊 Summary:")
    print(f"   - Downloads: {len(downloads_data)} items")
    print(f"   - Products: {len(products_data)} items")
    print("\n🚀 You can now start using the application!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
