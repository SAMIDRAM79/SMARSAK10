from fastapi import APIRouter, HTTPException, status
from models import Product, ProductCreate
from database import get_db
from utils import serialize_doc
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=List[dict])
async def get_products():
    """Get all active products"""
    db = get_db()
    
    products = await db.products.find({"active": True}).to_list(100)
    return [serialize_doc(product) for product in products]

@router.get("/{product_id}", response_model=dict)
async def get_product(product_id: str):
    """Get a specific product"""
    db = get_db()
    
    from bson import ObjectId
    try:
        product = await db.products.find_one({"_id": ObjectId(product_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return serialize_doc(product)

@router.post("", response_model=dict)
async def create_product(product: ProductCreate):
    """Create a new product (admin only)"""
    db = get_db()
    
    product_dict = product.model_dump()
    result = await db.products.insert_one(product_dict)
    
    return {
        "id": str(result.inserted_id),
        "message": "Product created successfully"
    }
