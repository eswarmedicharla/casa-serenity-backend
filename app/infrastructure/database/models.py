from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime
from .db import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True)
    mobile_number = Column(String(20))
    gender = Column(String(10))
    profession = Column(String(100))
    date_of_birth = Column(Date)
    password = Column(String(255))
    role = Column(String(50), default="USER")
    created_at = Column(DateTime, default=datetime.utcnow)