from fastapi import APIRouter, Depends, HTTPException, status, Header
from app.models import User
from app.database import user_collection
from app.utils import verify_token
from bson.objectid import ObjectId
from app.endpoints.auth import get_password_hash
import logging
from app.auth import require_role

logger = logging.getLogger(__name__)

router = APIRouter()

# Dependency to get the current user from the JWT token
def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
        )
    token = authorization.split(" ")[1]  # Extract token after "Bearer"
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return payload  # Returning token payload for now; you could return more user info later

# Get the current user details (Only authenticated user can access)
@router.get("/me", response_model=User)
async def get_user_me(current_user: dict = Depends(get_current_user)):
    logger.info(f"Fetching details for user: {current_user['username']}")
    db_user = user_collection.find_one({"_id": ObjectId(current_user["sub"])})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(username=db_user["username"], email=db_user["email"], password="")

# Update the user's information (Only authenticated user can update their own details)
@router.put("/me", response_model=User)
async def update_user_me(user: User, current_user: dict = Depends(get_current_user)):
    db_user = user_collection.find_one({"_id": ObjectId(current_user["sub"])})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = {
        "username": user.username,
        "email": user.email,
        "password": get_password_hash(user.password),  # Hashing password again
    }
    user_collection.update_one({"_id": ObjectId(current_user["sub"])}, {"$set": updated_user})
    return user

# Delete the user's account (Only authenticated user can delete their own account)
@router.delete("/me", response_model=dict)
async def delete_user_me(current_user: dict = Depends(get_current_user)):
    user_id = current_user["sub"]  # Extracting the user ID from the token
    db_user = user_collection.find_one({"_id": ObjectId(user_id)})  # Querying the database
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_collection.delete_one({"_id": ObjectId(user_id)})
    return {"message": "User deleted successfully"}

@router.get("/all", response_model=list[User])
async def get_all_users(current_user: dict = Depends(require_role("admin"))):
    logger.info(f"Admin {current_user['username']} is fetching all users")

    users = user_collection.find({})
    return [
        User(username=u["username"], email=u["email"], password="", role=u["role"])
        for u in users
    ]