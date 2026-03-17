from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.infrastructure.database.models import TokenBlacklist
from datetime import datetime

class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def blacklist_token(self, token: str, expires_at: datetime):
    # Executes: INSERT INTO token_blacklist (token, expires_at, created_at) VALUES (...)
        stmt = insert(TokenBlacklist).values(
            token=token,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
        await self.db.execute(stmt)
        await self.db.commit()