from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import Optional

class Database:
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls.client is None:
            mongo_url = os.environ.get('MONGO_URL')
            cls.client = AsyncIOMotorClient(mongo_url)
        return cls.client
    
    @classmethod
    def get_database(cls):
        client = cls.get_client()
        db_name = os.environ.get('DB_NAME', 'smartscool')
        return client[db_name]
    
    @classmethod
    def close_connection(cls):
        if cls.client:
            cls.client.close()
            cls.client = None

def get_db():
    return Database.get_database()
