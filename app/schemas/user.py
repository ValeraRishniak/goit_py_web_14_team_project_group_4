from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from app.database.models import Role

class UserModel(BaseModel):
    username: str = Field(min_length=4, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=16)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str
    role: Role

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    is_active: bool | None
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr

class RequestRole(BaseModel):
    email: EmailStr
    role: Role
