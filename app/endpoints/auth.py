from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import create_access_token
from app.database import user_collection
from app.models import User, Token
from bson.objectid import ObjectId
from passlib.context import CryptContext
import logging



logger = logging.getLogger(__name__)
router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/login", response_model=Token)
async def login(user: User):
    logger.info(f"Attempting login for user: {user.email}")
    db_user = user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = {"sub": str(db_user["_id"]), "username": db_user["username"]}
    access_token = create_access_token(data=token_data)
    logger.info(f"User {user.email} logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register", response_model=User)
async def register(user: User):
    logger.info(f"Registering new user: {user.email}")
    db_user = user_collection.find_one({"email": user.email})
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # Hash the password before storing it
    hashed_password = get_password_hash(user.password)
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "role": user.role,
    }
    # Insert the new user into MongoDB
    user_collection.insert_one(new_user)
    logger.info(f"User {user.email} registered successfully")
    return user
