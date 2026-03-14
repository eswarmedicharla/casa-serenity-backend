from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"

def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(hours=2)

    payload.update({"exp": expire})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)