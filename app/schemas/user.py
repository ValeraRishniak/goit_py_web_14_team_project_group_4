from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

from app.database.models import Role


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=16)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb

    detail: str = "User successfully created"


class UserProfileModel(BaseModel):
    username: str
    email: EmailStr
    avatar: Optional[str]
    foto_count: Optional[int]
    comment_count: Optional[int]
    is_active: Optional[bool]
    created_at: datetime


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class RequestRole(BaseModel):
    email: EmailStr
    role: Role
