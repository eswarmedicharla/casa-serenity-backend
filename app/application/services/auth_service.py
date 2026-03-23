from app.utils.password import hash_password, verify_password
from app.core.security import create_access_token, decode_token
from app.domain.enums.roles import RoleEnum
from fastapi import HTTPException
from datetime import datetime, timedelta

class AuthService:

    def __init__(self, user_repo, token_repo=None):
        self.user_repo = user_repo
        self.token_repo = token_repo

    # ✅ SYNC
    def register_user(self, data: dict):
        if data["password"] != data.get("confirmPassword"):
            raise HTTPException(status_code=400, detail="Passwords do not match")

        existing = self.user_repo.get_by_email(data["email"])
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        try:
            role = RoleEnum(data["role"])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid role")

        hashed_password = hash_password(data["password"])

        user_data = {
            "name": data["name"],
            "email": data["email"],
            "mobileNumber": data["mobileNumber"],
            "gender": data["gender"],
            "profession": data["profession"],
            "dateOfBirth": data["dateOfBirth"],
            "password": hashed_password,
            "confirmPassword": data["confirmPassword"],
            "roleId": role.value
        }

        user = self.user_repo.create(user_data)

        return {
            "message": "User registered successfully",
            "role": role.name,
            "user_id": user.id
        }

    # ✅ SYNC
    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = create_access_token({
            "user_id": user.id,
            "role": user.roleId
        })

        return {
            "access_token": token,
            "role": user.role.name if user.role else "Unknown",
            "user_id": user.id
        }

    # ✅ SYNC
    def logout(self, token: str, current_user_id: int):
        if not self.token_repo:
            raise HTTPException(status_code=500, detail="Token repository not initialized")

        payload = decode_token(token)
        exp_timestamp = payload.get("exp")

        if exp_timestamp:
            expires_at = datetime.utcfromtimestamp(exp_timestamp)
        else:
            expires_at = datetime.utcnow() + timedelta(hours=24)

        self.token_repo.blacklist_token(token, expires_at)

        return {"message": "Successfully logged out. Token invalidated."}