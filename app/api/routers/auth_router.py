from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.db import get_db
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.repositories.token_repository import TokenRepository
from app.application.services.auth_service import AuthService
from app.api.schemas.auth_schema import RegisterRequest, LoginRequest
from app.core.security import get_current_active_user
from fastapi.security import HTTPAuthorizationCredentials
from app.core import security

router = APIRouter()

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService(UserRepository(db)).register_user(request.dict())

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return AuthService(UserRepository(db)).login(request.email, request.password)

@router.get("/profile")
def profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    service = AuthService(UserRepository(db))
    return service.get_profile(current_user.get("user_id"))

@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security.security),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    token = credentials.credentials
    service = AuthService(UserRepository(db), TokenRepository(db))
    return service.logout(token, current_user.get("user_id"))

@router.put("/users/{user_id}/status")
def update_status(
    user_id: int,
    status: int,
    db: Session = Depends(get_db)
):
    service = AuthService(UserRepository(db))
    return service.update_user_status(user_id, status)