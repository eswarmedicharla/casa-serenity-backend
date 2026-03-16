from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


class RoleModel(Base):

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("UserModel", back_populates="role")


class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    email = Column(String(150), unique=True, index=True)

    mobileNumber = Column(String(20))

    gender = Column(String(10))

    profession = Column(String(100))

    dateOfBirth = Column(Date)

    password = Column(String(255))

    confirmPassword = Column(String(255))

    roleId = Column(Integer, ForeignKey("roles.id"))

    createdAt = Column(DateTime, default=datetime.utcnow)

    role = relationship("RoleModel", back_populates="users")