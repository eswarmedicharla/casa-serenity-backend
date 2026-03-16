# app/application/services/auth_service.py

from app.utils.password import hash_password, verify_password
from app.core.security import create_access_token
from app.domain.enums.roles import RoleEnum


class AuthService:

    def __init__(self, repo):
        self.repo = repo


    def register_user(self, data):

        if data["password"] != data["confirmPassword"]:
            raise Exception("Passwords do not match")

        existing = self.repo.get_by_email(data["email"])
        if existing:
            raise Exception("Email already exists")

        # validate role using enum
        try:
            role = RoleEnum(data["role"])
        except ValueError:
            raise Exception("Invalid role")

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

        user = self.repo.create(user_data)

        token = create_access_token({
            "user_id": user.id,
            "role": role.value
        })

        return {
            "message": "User registered successfully",
            "access_token": token,
            "role": role.name
        }

    def login(self, email, password):

        user = self.repo.get_by_email(email)

        if not user:
            raise Exception("Invalid email")

        if not verify_password(password, user.password):
            raise Exception("Invalid password")

        token = create_access_token({
            "userId": user.id,
            "role": user.roleId
        })

        return {
            "access_token": token,
            "role": user.role.name
        }