from app.utils.password import hash_password, verify_password
from app.core.security import create_access_token


class AuthService:

    def __init__(self, repo):

        self.repo = repo


    def register_user(self, data):

        if data["password"] != data["confirm_password"]:
            raise Exception("Passwords do not match")

        existing = self.repo.get_by_email(data["email"])

        if existing:
            raise Exception("Email already exists")

        data["password"] = hash_password(data["password"])

        user_data = {
            "name": data["name"],
            "email": data["email"],
            "mobile_number": data["mobile_number"],
            "gender": data["gender"],
            "profession": data["profession"],
            "date_of_birth": data["date_of_birth"],
            "password": data["password"],
            "role": "USER"
        }

        user = self.repo.create(user_data)

        token = create_access_token({"user_id": user.id})

        return {
            "message": "User registered successfully",
            "access_token": token
        }


    def login(self, email, password):

        user = self.repo.get_by_email(email)

        if not user:
            raise Exception("Invalid email")

        if not verify_password(password, user.password):
            raise Exception("Invalid password")

        token = create_access_token({"user_id": user.id})

        return {
            "access_token": token
        }