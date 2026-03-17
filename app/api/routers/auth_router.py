from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

# Import the security module and the NEW dependency
from app.core import security
from app.core.security import get_current_active_user 

from app.infrastructure.database.db import get_db
from app.infrastructure.repositories.token_repository import TokenRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.services.auth_service import AuthService
from app.api.schemas.auth_schema import RegisterRequest, LoginRequest

router = APIRouter()

@router.post("/register")
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    # Note: TokenRepo not needed for registration
    service = AuthService(user_repo, None) 
    return await service.register_user(request.dict())

@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    service = AuthService(user_repo, None)
    return await service.login(request.email, request.password)

@router.get("/profile")
async def get_profile(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user) # Use the new dependency
):
    user_repo = UserRepository(db)
    user_id = current_user.get("user_id")
    
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "mobileNumber": user.mobileNumber,
        "gender": user.gender,
        "profession": user.profession,
        "dateOfBirth": user.dateOfBirth,
        "role": user.role.name if user.role else None,
        "createdAt": user.createdAt
    }

@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security.security), 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    token = credentials.credentials
    user_repo = UserRepository(db)
    token_repo = TokenRepository(db)
    
    # Pass both repos to the service
    service = AuthService(user_repo, token_repo)
    
    return await service.logout(token, current_user.get("user_id"))