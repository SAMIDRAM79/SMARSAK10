from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import Optional
import re

class Database:
    client: Optional[AsyncIOMotorClient] = None
    _db_name: Optional[str] = None
    
    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls.client is None:
            mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
            cls.client = AsyncIOMotorClient(mongo_url)
            
            # Extract and store database name from URL if present
            if cls._db_name is None:
                db_name_from_url = None
                if '//' in mongo_url and '/' in mongo_url.split('//', 1)[1]:
                    url_parts = mongo_url.split('//', 1)[1].split('/', 1)
                    if len(url_parts) > 1:
                        db_name_part = url_parts[1].split('?')[0]
                        if db_name_part and db_name_part not in ['', 'test']:
                            db_name_from_url = db_name_part
                
                cls._db_name = db_name_from_url or os.environ.get('DB_NAME', 'smartscool')
        
        return cls.client
    
    @classmethod
    def get_database(cls):
        client = cls.get_client()
        return client[cls._db_name]
    
    @classmethod
    def close_connection(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            cls._db_name = None

def get_db():
    return Database.get_database()
