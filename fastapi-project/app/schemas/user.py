"""
Pydantic schemas for User-related requests and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ---------- Request Schemas ----------

class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=50, examples=["john_doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., min_length=6, max_length=100, examples=["securepass123"])
    full_name: Optional[str] = Field(None, max_length=100, examples=["John Doe"])


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str = Field(..., examples=["john_doe"])
    password: str = Field(..., examples=["securepass123"])


# ---------- Response Schemas ----------

class UserResponse(BaseModel):
    """Schema for user data returned in API responses."""
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------- Token Schemas ----------

class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data extracted from a JWT token."""
    username: Optional[str] = None
