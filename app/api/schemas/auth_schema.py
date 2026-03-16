from pydantic import BaseModel, EmailStr
from datetime import date
from app.domain.enums.roles import RoleEnum


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    mobileNumber: str
    gender: str
    profession: str
    role: RoleEnum
    dateOfBirth: date
    password: str
    confirmPassword: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str