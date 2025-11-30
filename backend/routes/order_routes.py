from fastapi import APIRouter, HTTPException, status, Depends
from models import Order, OrderCreate, OrderStatus
from database import get_db
from utils import serialize_doc, generate_order_number
from auth import get_current_user
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=dict)
async def create_order(order: OrderCreate):
    """Create a new order"""
    db = get_db()
    
    # Generate order number
    order_number = generate_order_number()
    
    # Create order document
    order_dict = order.model_dump()
    order_dict["order_number"] = order_number
    order_dict["status"] = OrderStatus.PENDING
    
    # Insert order
    result = await db.orders.insert_one(order_dict)
    
    return {
        "id": str(result.inserted_id),
        "order_number": order_number,
        "status": OrderStatus.PENDING,
        "message": "Commande créée avec succès"
    }

@router.get("", response_model=List[dict])
async def get_orders(current_user: dict = Depends(get_current_user)):
    """Get all orders (admin only)"""
    db = get_db()
    
    orders = await db.orders.find().sort("created_at", -1).to_list(100)
    return [serialize_doc(order) for order in orders]

@router.get("/{order_id}", response_model=dict)
async def get_order(order_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific order"""
    db = get_db()
    
    try:
        order = await db.orders.find_one({"_id": ObjectId(order_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return serialize_doc(order)

@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: str,
    status: OrderStatus,
    current_user: dict = Depends(get_current_user)
):
    """Update order status (admin only)"""
    db = get_db()
    
    try:
        result = await db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": status}}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return {"message": "Order status updated successfully"}
