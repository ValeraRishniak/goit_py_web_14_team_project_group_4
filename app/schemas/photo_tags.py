from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl

from app.schemas.tags import ImageTagResponse
# class TagPhoto(BaseModel):
#     name: str   = Field(max_length=25)
    
# class TagPhotoResponse(TagPhoto):
#     id: int

#     class Config:
#         from_attributes = True

class PhotoBase(BaseModel):
     url: HttpUrl
     name: str

class PhotoModels(PhotoBase):
    description: str | None = None
    photo: PhotoBase | None = None
    tags: List[ImageTagResponse]
    id  : int
     
    class Config:
        from_attributes = True





