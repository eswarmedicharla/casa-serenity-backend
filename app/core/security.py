from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta
import uuid

from app.infrastructure.database.models import TokenBlacklist
from app.infrastructure.database.db import get_db
from app.utils.exceptions import AppException

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

security = HTTPBearer()

def create_access_token(data: dict):
    payload = data.copy()
    payload.update({
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "jti": str(uuid.uuid4())
    })
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise AppException.token_invalid()

def get_current_active_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_token(token)

    stmt = select(TokenBlacklist).where(TokenBlacklist.token == token)
    if db.execute(stmt).scalars().first():
        raise AppException.token_blacklisted()

    return payload