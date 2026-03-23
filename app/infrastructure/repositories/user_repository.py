from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session
from app.infrastructure.database.models import UserModel

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.role))
            .where(UserModel.email == email)
        )
        result = self.db.execute(stmt)
        return result.scalars().first()

    def get_by_id(self, user_id: int):
        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.role))
            .where(UserModel.id == user_id)
        )
        result = self.db.execute(stmt)
        return result.scalars().first()

    def create(self, data: dict):
        user = UserModel(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # load relationship explicitly
        self.db.refresh(user, attribute_names=["role"])

        return user