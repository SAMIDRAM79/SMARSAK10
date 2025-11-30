from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone

# Import routes
from routes import (
    student_routes,
    classe_routes,
    matiere_routes,
    note_routes,
    bulletin_routes,
    stats_routes,
    enseignant_routes
)


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

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

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()