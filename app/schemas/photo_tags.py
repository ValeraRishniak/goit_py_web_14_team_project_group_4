from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class ImageTagModel(BaseModel):
    tag_name: str = Field(max_length=25)


class ImageTagResponse(ImageTagModel):
    id: int

    class Config:
        orm_mode = True


class PhotoBase(BaseModel):
    url: HttpUrl
    name: str


class PhotoModels(PhotoBase):
    description: str | None = None
    photo: PhotoBase | None = None
    tags: List[ImageTagResponse]
    id: int

    class Config:
        from_attributes = True
