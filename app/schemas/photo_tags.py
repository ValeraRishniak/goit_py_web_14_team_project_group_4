from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class TagPhoto(BaseModel):
    name: str   = Field(max_length=25)
    
class TagPhotoResponse(TagPhoto):
    id: int

    class Config:
        from_attributes = True




class PhotoBase(BaseModel):
     url: HttpUrl
     name: str

class PhotoModels(PhotoBase):
    description: str | None = None
    photo: PhotoBase | None = None
    tags: List[TagPhotoResponse]
    id  : int
     
    class Config:
        from_attributes = True





