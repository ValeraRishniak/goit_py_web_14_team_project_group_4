from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    comment_description: str


class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    user_id: int
    image_id: int
    update_status: bool = False

    class Config:
        from_attributes = True


class CommentUpdateResponse(CommentBase):
    updated_at: datetime
    update_status: bool = True

    class Config:
        from_attributes = True
