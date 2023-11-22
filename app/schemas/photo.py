from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from app.schemas.comment import CommentResponse
from app.schemas.tags import ImageTagModel, ImageTagResponse


class ImageModel(BaseModel):
    title: str = Field(max_length=45)
    description: str = Field(max_length=255)
    tags: List[ImageTagModel]

    @field_validator("tags")
    def validate_tags(cls, v):
        """
        The validate_tags function is a class method that validates the tags field.
        It ensures that no more than 5 tags are added to a post.
        
        :param cls: Pass the class object to the function
        :param v: Pass the value of the tags field
        :return: The value of v, which is a list
        """
        
        if len(v or []) > 5:
            raise ValueError("Too many tags. Maximum 5 tags allowed.")
        return v


class ImageModelsResponse(ImageModel):
    tags: List[ImageTagResponse]
    image_url: str = Field(max_length=300, default=None)
    transform_url: str | None = Field(max_length=300, default=None)
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ImageWithCommentModelsResponse(ImageModel):
    tags: List[ImageTagResponse]
    comment: List[CommentResponse]
    image_url: str = Field(max_length=300, default=None)
    transform_url: str | None = Field(max_length=300, default=None)
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
