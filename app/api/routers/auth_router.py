from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.db import SessionLocal
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.services.auth_service import AuthService

from app.api.schemas.auth_schema import RegisterRequest, LoginRequest

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):

    repo = UserRepository(db)

    service = AuthService(repo)

    return service.register_user(request.dict())


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):

    repo = UserRepository(db)

    service = AuthService(repo)

    return service.login(request.email, request.password)