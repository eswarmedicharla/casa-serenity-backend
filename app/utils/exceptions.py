from fastapi import HTTPException, status

class AppException:

    @staticmethod
    def invalid_credentials():
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    @staticmethod
    def user_not_found():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    @staticmethod
    def email_already_exists():
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    @staticmethod
    def password_mismatch():
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    @staticmethod
    def invalid_role():
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")

    @staticmethod
    def token_invalid():
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    @staticmethod
    def token_blacklisted():
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")

    @staticmethod
    def server_error():
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    @staticmethod
    def user_not_active():
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive or blocked")

    @staticmethod
    def invalid_status():
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status value")