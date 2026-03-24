from sqlalchemy.orm import Session
from sqlalchemy import insert
from datetime import datetime
from app.infrastructure.database.models import TokenBlacklist

class TokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def blacklist_token(self, token: str, expires_at: datetime):
        stmt = insert(TokenBlacklist).values(
            token=token,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
        self.db.execute(stmt)
        self.db.commit()