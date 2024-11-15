import jwt
from app.config import settings

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  
    except jwt.InvalidTokenError:
        return None  
