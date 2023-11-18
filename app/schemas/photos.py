"""
variant VRishniak
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


from app.schemas.tags import ImageTagResponse


class ImageModel(BaseModel):
    image_url: str = Field(max_length=300, default=None)
    title: str = Field(max_length=45)
    description: str = Field(max_length=255)
    tags: List[str] = []


class ImageResponse(ImageModel):
    id: int
    avg_rating: Optional[float] = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
