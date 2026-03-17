from sqlalchemy import select
from sqlalchemy.orm import selectinload  # Import this
from app.infrastructure.database.models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str):
        # Use selectinload to eagerly load the 'role' relationship
        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.role))
            .where(UserModel.email == email)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_id(self, user_id: int):
        # Use selectinload here as well for get_profile
        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.role))
            .where(UserModel.id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, data: dict):
        user = UserModel(**data)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        # If you need the role immediately after creation, you might need to reload it 
        # or ensure roleId is set correctly. Usually refresh() works for simple columns, 
        # but for relationships, explicit loading is safer if accessed immediately.
        # However, for login/register flow, the role is usually set by ID, so accessing 
        # user.role might still trigger a load if not careful. 
        # For 'create', let's ensure we return the object. 
        # If you access user.role immediately after create, you might need:
        await self.db.refresh(user, attribute_names=['role']) 
        return user