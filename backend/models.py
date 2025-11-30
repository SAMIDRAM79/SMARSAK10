from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Enums
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class DownloadType(str, Enum):
    KIT_COMPLET = "kit_complet"
    MISE_A_JOUR = "mise_a_jour"
    ANCIENNE_VERSION = "ancienne_version"

# User Models
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: str
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Download Models
class DownloadBase(BaseModel):
    name: str
    version: str
    size: str
    type: DownloadType
    file_url: str
    release_date: datetime

class DownloadCreate(DownloadBase):
    pass

class Download(DownloadBase):
    id: str
    downloads: int = 0

    class Config:
        from_attributes = True

class DownloadTrack(BaseModel):
    download_id: str
    user_id: Optional[str] = None

# Product Models
class ProductBase(BaseModel):
    name: str
    description: str
    features: List[str]
    image: str
    price: Optional[float] = None

class ProductCreate(ProductBase):
    active: bool = True

class Product(ProductBase):
    id: str
    active: bool = True

    class Config:
        from_attributes = True

# Order Models
class OrderBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    company: Optional[str] = None
    product: str
    quantity: int = 1
    message: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: str
    order_number: str
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

# Ticket Models
class TicketBase(BaseModel):
    name: str
    email: EmailStr
    subject: str
    priority: TicketPriority
    description: str

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: str
    ticket_number: str
    status: TicketStatus = TicketStatus.OPEN
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
