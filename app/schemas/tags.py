"""
variant VRishniak
"""


from datetime import datetime
from pydantic import BaseModel, Field


class ImageTagModel(BaseModel):
    tag_name: str = Field(max_length=25)


class ImageTagResponse(ImageTagModel):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
