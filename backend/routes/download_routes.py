from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from models import Download, DownloadTrack
from database import get_db
from utils import serialize_doc
from typing import List
import os

router = APIRouter(prefix="/downloads", tags=["downloads"])

@router.get("", response_model=List[dict])
async def get_downloads():
    """Get all available downloads"""
    db = get_db()
    
    downloads = await db.downloads.find().to_list(100)
    return [serialize_doc(download) for download in downloads]

@router.post("/track")
async def track_download(track: DownloadTrack):
    """Track a download"""
    db = get_db()
    
    # Get download info
    download = await db.downloads.find_one({"_id": track.download_id})
    if not download:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Download not found"
        )
    
    # Increment download count
    await db.downloads.update_one(
        {"_id": track.download_id},
        {"$inc": {"downloads": 1}}
    )
    
    # Log download
    download_log = {
        "download_id": track.download_id,
        "user_id": track.user_id,
        "downloaded_at": None
    }
    await db.download_logs.insert_one(download_log)
    
    return {
        "success": True,
        "download_url": download["file_url"],
        "message": "Téléchargement prêt"
    }

@router.get("/file/{filename}")
async def download_file(filename: str):
    """Download a file"""
    file_path = f"/app/backend/uploads/downloads/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )
