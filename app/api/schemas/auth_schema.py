from pydantic import BaseModel, EmailStr
from datetime import date
from app.domain.enums.roles import RoleEnum


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    mobile_number: str
    gender: str
    profession: str
    role: RoleEnum
    date_of_birth: date
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str