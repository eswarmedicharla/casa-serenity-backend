from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("UserModel", back_populates="role")


class StatusModel(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("UserModel", back_populates="status")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)

    mobile_number = Column(String(20))
    gender = Column(String(10))
    profession = Column(String(100))
    date_of_birth = Column(Date)

    password = Column(String(255), nullable=False)
    confirm_password = Column(String(255), nullable=False)  # ✅ Added
    # ✅ FIXED naming
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False, default=1)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    role = relationship("RoleModel", back_populates="users")
    status = relationship("StatusModel", back_populates="users")


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)