from fastapi import APIRouter, HTTPException, status, Depends
from models import Ticket, TicketCreate, TicketStatus
from database import get_db
from utils import serialize_doc, generate_ticket_number
from auth import get_current_user
from typing import List
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("", response_model=dict)
async def create_ticket(ticket: TicketCreate):
    """Create a new support ticket"""
    db = get_db()
    
    # Generate ticket number
    ticket_number = generate_ticket_number()
    
    # Create ticket document
    ticket_dict = ticket.model_dump()
    ticket_dict["ticket_number"] = ticket_number
    ticket_dict["status"] = TicketStatus.OPEN
    ticket_dict["created_at"] = datetime.utcnow()
    ticket_dict["updated_at"] = datetime.utcnow()
    
    # Insert ticket
    result = await db.tickets.insert_one(ticket_dict)
    
    return {
        "id": str(result.inserted_id),
        "ticket_number": ticket_number,
        "status": TicketStatus.OPEN,
        "message": "Ticket créé avec succès. Notre équipe vous contactera bientôt."
    }

@router.get("", response_model=List[dict])
async def get_tickets(current_user: dict = Depends(get_current_user)):
    """Get all tickets (admin only)"""
    db = get_db()
    
    tickets = await db.tickets.find().sort("created_at", -1).to_list(100)
    return [serialize_doc(ticket) for ticket in tickets]

@router.get("/{ticket_id}", response_model=dict)
async def get_ticket(ticket_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific ticket"""
    db = get_db()
    
    try:
        ticket = await db.tickets.find_one({"_id": ObjectId(ticket_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    return serialize_doc(ticket)

@router.patch("/{ticket_id}/status")
async def update_ticket_status(
    ticket_id: str,
    status: TicketStatus,
    current_user: dict = Depends(get_current_user)
):
    """Update ticket status (admin only)"""
    db = get_db()
    
    try:
        result = await db.tickets.update_one(
            {"_id": ObjectId(ticket_id)},
            {"$set": {
                "status": status,
                "updated_at": datetime.utcnow()
            }}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    return {"message": "Ticket status updated successfully"}
