from fastapi import APIRouter, HTTPException, status, Depends
from models import Note, NoteCreate
from database import get_db
from utils import serialize_doc
from auth_middleware import verify_email
from typing import List
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("", response_model=dict)
async def create_note(note: NoteCreate, email: str = Depends(verify_email)):
    """Créer une nouvelle note"""
    db = get_db()
    
    # Vérifier que la note ne dépasse pas le maximum
    if note.note > note.note_sur:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La note ne peut pas dépasser {note.note_sur}"
        )
    
    note_dict = note.model_dump()
    note_dict["date_saisie"] = datetime.utcnow()
    
    result = await db.notes.insert_one(note_dict)
    
    return {
        "id": str(result.inserted_id),
        "message": "Note enregistrée avec succès"
    }

@router.get("/student/{student_id}", response_model=List[dict])
async def get_student_notes(
    student_id: str,
    email: str = Depends(verify_email),
    periode: str = None
):
    """Récupérer les notes d'un élève"""
    db = get_db()
    
    query = {"student_id": student_id}
    if periode:
        query["periode"] = periode
    
    notes = await db.notes.find(query).sort("date_saisie", -1).to_list(1000)
    
    # Enrichir avec les infos des matières
    result = []
    for note in notes:
        note_doc = serialize_doc(note)
        matiere = await db.matieres.find_one({"_id": ObjectId(note["matiere_id"])})
        if matiere:
            note_doc["matiere_nom"] = matiere["nom"]
        result.append(note_doc)
    
    return result

@router.get("/classe/{classe}", response_model=List[dict])
async def get_classe_notes(
    classe: str,
    email: str = Depends(verify_email),
    matiere_id: str = None,
    periode: str = None
):
    """Récupérer les notes d'une classe"""
    db = get_db()
    
    # Récupérer les élèves de la classe
    students = await db.students.find({"classe": classe, "statut": "actif"}).to_list(1000)
    student_ids = [str(s["_id"]) for s in students]
    
    query = {"student_id": {"$in": student_ids}}
    if matiere_id:
        query["matiere_id"] = matiere_id
    if periode:
        query["periode"] = periode
    
    notes = await db.notes.find(query).to_list(1000)
    return [serialize_doc(note) for note in notes]

@router.put("/{note_id}", response_model=dict)
async def update_note(note_id: str, note: NoteCreate, email: str = Depends(verify_email)):
    """Mettre à jour une note"""
    db = get_db()
    
    if note.note > note.note_sur:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La note ne peut pas dépasser {note.note_sur}"
        )
    
    try:
        result = await db.notes.update_one(
            {"_id": ObjectId(note_id)},
            {"$set": note.model_dump()}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID invalide"
        )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note non trouvée"
        )
    
    return {"message": "Note mise à jour avec succès"}

@router.delete("/{note_id}")
async def delete_note(note_id: str, email: str = Depends(verify_email)):
    """Supprimer une note"""
    db = get_db()
    
    try:
        result = await db.notes.delete_one({"_id": ObjectId(note_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID invalide"
        )
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note non trouvée"
        )
    
    return {"message": "Note supprimée avec succès"}
