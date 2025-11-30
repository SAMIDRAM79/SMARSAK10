from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import routes
from routes import (
    student_routes,
    classe_routes,
    matiere_routes,
    note_routes,
    bulletin_routes,
    stats_routes,
    enseignant_routes,
    parametres_routes,
    import_routes,
    centres_routes
)
from routes import repartition_routes


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env', override=False)

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')

# Extract database name from MONGO_URL if it contains one, otherwise use DB_NAME env var
# MongoDB Atlas URLs format: mongodb+srv://user:pass@host/database_name?options
import re
db_name_from_url = None
if '//' in mongo_url and '/' in mongo_url.split('//', 1)[1]:
    # Extract database name from URL
    url_parts = mongo_url.split('//', 1)[1].split('/', 1)
    if len(url_parts) > 1:
        db_name_part = url_parts[1].split('?')[0]  # Remove query parameters
        if db_name_part and db_name_part not in ['', 'test']:
            db_name_from_url = db_name_part

# Use database name from URL if available, otherwise from environment variable
db_name = db_name_from_url or os.environ.get('DB_NAME', 'smartscool')

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Create the main app without a prefix
app = FastAPI(title="SMARTSAK10 - Gestion Scolaire", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Add root endpoint
@api_router.get("/")
async def root():
    return {
        "application": "SMARTSAK10",
        "version": "1.0.0",
        "description": "Système de gestion scolaire complet",
        "status": "running"
    }

@api_router.get("/health")
async def health_check():
    """Health check endpoint to verify MongoDB connection"""
    try:
        # Try to ping MongoDB
        await db.command('ping')
        return {
            "status": "healthy",
            "database": "connected",
            "db_name": db.name
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

# Add CORS middleware FIRST (before routes)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
api_router.include_router(student_routes.router)
api_router.include_router(classe_routes.router)
api_router.include_router(matiere_routes.router)
api_router.include_router(note_routes.router)
api_router.include_router(bulletin_routes.router)
api_router.include_router(stats_routes.router)
api_router.include_router(enseignant_routes.router)

# Include the router in the main app
app.include_router(api_router)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()