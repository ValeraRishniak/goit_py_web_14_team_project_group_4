from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class ImageTagModel(BaseModel):
    tag_name: str = Field(max_length=25)


class ImageTagResponse(ImageTagModel):
    id: int

    class Config:
        from_attributes = True


class PhotoBase(BaseModel):
     url: str
     name: str | None = None

class PhotoModels(PhotoBase):
    description: str | None = None
    photo: PhotoBase | None = None
    tags: List[ImageTagResponse] | None = None
    id  : int
     
    class Config:
        from_attributes = True





