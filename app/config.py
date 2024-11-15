from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    mongo_uri: str = os.getenv("MONGO_URI")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")

settings = Settings()
