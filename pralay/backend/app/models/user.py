"""
User and Role-Based Access Control Model
Supports: Admin, NDRF Officer, District Magistrate (DM) Official, View-only
"""

from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
import enum

from app.models import BaseModel


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    NDRF_OFFICER = "ndrf_officer"
    DM_OFFICIAL = "dm_official"
    VIEW_ONLY = "view_only"


class User(BaseModel):
    """Authority or operator user account"""
    __tablename__ = "users"

    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    
    role = Column(SQLEnum(UserRole), default=UserRole.DM_OFFICIAL, nullable=False)
    jurisdiction_district = Column(String(100), nullable=True)  # e.g. "Chamoli", "Rudraprayag"
    phone_number = Column(String(50), nullable=True)
    
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
