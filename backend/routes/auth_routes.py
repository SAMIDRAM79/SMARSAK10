from fastapi import APIRouter, HTTPException, status, Depends
from models import UserCreate, UserLogin, User, Token, UserInDB
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from database import get_db
from utils import serialize_doc
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=dict)
async def register(user: UserCreate):
    """Register a new user"""
    db = get_db()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user document
    user_dict = user.model_dump()
    hashed_password = get_password_hash(user_dict.pop("password"))
    user_dict["hashed_password"] = hashed_password
    user_dict["role"] = "user"
    
    # Insert user
    result = await db.users.insert_one(user_dict)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(days=7)
    )
    
    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "email": user.email,
        "token": access_token
    }

@router.post("/login", response_model=dict)
async def login(user_login: UserLogin):
    """Login user"""
    db = get_db()
    
    # Find user
    user = await db.users.find_one({"email": user_login.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(user_login.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=timedelta(days=7)
    )
    
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "token": access_token
    }

@router.get("/me", response_model=dict)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    db = get_db()
    
    user = await db.users.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = serialize_doc(user)
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "phone": user.get("phone"),
        "company": user.get("company")
    }
