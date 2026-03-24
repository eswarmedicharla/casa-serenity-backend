from app.domain.enums.userStatus import UserStatusEnum
from app.utils.password import hash_password, verify_password
from app.core.security import create_access_token, decode_token
from app.domain.enums.roles import RoleEnum
from datetime import datetime, timedelta
from app.utils.exceptions import AppException
from app.utils.response import success_response


class AuthService:

    def __init__(self, user_repo, token_repo=None):
        self.user_repo = user_repo
        self.token_repo = token_repo

    def register_user(self, data: dict):
        if data["password"] != data.get("confirm_password"):
            raise AppException.password_mismatch()

        existing = self.user_repo.get_by_email(data["email"])
        if existing:
            raise AppException.email_already_exists()

        try:
            role = RoleEnum(data["role"])
        except ValueError:
            raise AppException.invalid_role()

        hashed_password = hash_password(data["password"])

        user = self.user_repo.create({
            "name": data["name"],
            "email": data["email"],
            "mobile_number": data["mobile_number"],
            "gender": data["gender"],
            "profession": data["profession"],
            "date_of_birth": data["date_of_birth"],
            "password": hashed_password,
            "confirm_password": data["confirm_password"],  # store as plain text
            "role_id": role.value,
            "status_id": UserStatusEnum.ACTIVE.value
        })

        return success_response(
            data={"user_id": user.id, "role": role.name},
            message="User registered successfully",
            code=201
        )

    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user or not verify_password(password, user.password):
            raise AppException.invalid_credentials()

        # ✅ Correct attribute
        if user.status_id != UserStatusEnum.ACTIVE.value:
            raise AppException.user_not_active()

        token = create_access_token({
            "user_id": user.id,
            "role": user.role_id
        })

        return success_response(
            data={
                "access_token": token,
                "user_id": user.id,
                "role": user.role.name if user.role else "Unknown"
            },
            message="Login successful"
        )

    def get_profile(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)

        if not user:
            raise AppException.user_not_found()

        return success_response(
            data={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "mobile_number": user.mobile_number,
                "gender": user.gender,
                "profession": user.profession,
                "date_of_birth": user.date_of_birth,
                "role": user.role.name if user.role else None,
                "created_at": user.created_at,
                "status": UserStatusEnum(user.status_id).name
            },
            message="Profile fetched successfully"
        )

    def logout(self, token: str, current_user_id: int):
        if not self.token_repo:
            raise AppException.server_error()

        payload = decode_token(token)
        exp = payload.get("exp")

        expires_at = datetime.utcfromtimestamp(exp) if exp else datetime.utcnow() + timedelta(hours=24)
        self.token_repo.blacklist_token(token, expires_at)

        return success_response(message="Successfully logged out")

    def update_user_status(self, user_id: int, status: int):
        user = self.user_repo.get_by_id(user_id)

        if not user:
            raise AppException.user_not_found()

        if status not in [e.value for e in UserStatusEnum]:
            raise AppException.invalid_status()

        # ✅ Fixed
        user.status_id = status

        self.user_repo.db.commit()

        return success_response(
            message="User status updated successfully"
        )