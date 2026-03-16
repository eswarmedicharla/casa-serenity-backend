from pydantic import BaseModel, EmailStr
from datetime import date


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    mobile_number: str
    gender: str
    profession: str
    role: str
    date_of_birth: date
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str