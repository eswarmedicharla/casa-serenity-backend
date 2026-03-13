from app.utils.password import hash_password, verify_password
from app.core.security import create_access_token


class AuthService:

    def __init__(self, repo):

        self.repo = repo


    def register(self, data):

        data["password"] = hash_password(data["password"])

        user = self.repo.create_user(data)

        token = create_access_token({"user_id": user.id})

        return {
            "access_token": token
        }


    def login(self, email, password):

        user = self.repo.get_user_by_email(email)

        if not user:

            raise Exception("User not found")

        if not verify_password(password, user.password):

            raise Exception("Invalid credentials")

        token = create_access_token({"user_id": user.id})

        return {
            "access_token": token
        }