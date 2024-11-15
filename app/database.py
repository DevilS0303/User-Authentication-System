 
from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.mongo_uri)
db = client["auth_system"]  # Choose a database name, like 'auth_system'
user_collection = db["users"]  # Collection for users
