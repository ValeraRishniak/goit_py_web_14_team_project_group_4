'''
variant VRishniak
'''

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.database.models import ImageTag



class ImageBase(BaseModel):
    id: int
    image_url: str = Field(max_length=300, default=None)
    title: str = Field(max_length=45)
    descr: str = Field(max_length=255)
    tags: List[str] = []


class ImageBaseModel(ImageBase):
    pass

    class Config:
        from_attributes = True


class ImageResponse(ImageBase):
    tags: List[ImageTag]
    avg_rating: Optional[float] = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
