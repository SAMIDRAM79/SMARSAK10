import random
import string
from datetime import datetime

def generate_order_number() -> str:
    """Generate a unique order number"""
    prefix = "ORD"
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}-{timestamp}-{random_suffix}"

def generate_ticket_number() -> str:
    """Generate a unique ticket number"""
    prefix = "TKT"
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}-{timestamp}-{random_suffix}"

def serialize_doc(doc: dict) -> dict:
    """Convert MongoDB document to JSON serializable format"""
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc
