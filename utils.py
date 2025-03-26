from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "db7db888fd9c8e356965811cd95c159c05cc9039c0a398e77570873a816bd443"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  
def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generates a JWT access token."""
    to_encode = data.copy()
    
    
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
