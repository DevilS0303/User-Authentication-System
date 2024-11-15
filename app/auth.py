import jwt
from datetime import datetime, timedelta
from app.config import settings
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from app.utils import verify_token
from app.database import user_collection
from bson.objectid import ObjectId
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    

def require_role(required_role: str):
    def role_dependency(token: str = Depends(oauth2_scheme)):  
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload["sub"]  
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user or user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )
        
        return user
    return role_dependency

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





    

