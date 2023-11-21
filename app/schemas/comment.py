from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    comment_description: str


class CommentResponse(CommentBase):
    id: int
    user_id: int
    created_at: datetime
    update_status: bool = False

    class Config:
        from_attributes = True


class CommentUpdateResponse(CommentBase):
    id: int
    updated_at: datetime
    update_status: bool = True

    class Config:
        from_attributes = True
