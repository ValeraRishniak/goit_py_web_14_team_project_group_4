'''
variant VRishniak
'''


from datetime import datetime
from pydantic import BaseModel, Field


class ImageTag(BaseModel):
    tag_name: str = Field(max_length=25)


class ImageTagModel(ImageTag):
    pass

    class Config:
        from_attributes = True


class ImageTagResponse(ImageTag):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
