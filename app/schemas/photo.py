"""
variant VRishniak
"""
from pydantic import BaseModel, validator
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.tags import ImageTagModel, ImageTagResponse


class ImageModel(BaseModel):
    title: str = Field(max_length=45)
    description: str = Field(max_length=255)
    tags: List[ImageTagModel]

    @validator("tags")
    def validate_tags(cls, v):
        if len(v or []) > 5:
            raise ValueError("Too many tags. Maximum 5 tags allowed.")
        return v


class ImageModelsResponse(ImageModel):
    tags: List[ImageTagResponse]
    image_url: str = Field(max_length=300, default=None)
    transform_url: str | None = Field(max_length=300, default=None)
    id: int
    avg_rating: Optional[float] = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# from datetime import datetime
# from typing import List, Optional
# from pydantic import BaseModel

# from app.schemas.tags import ImageTagResponse


# class ImageBase(BaseModel):
#     name: str | None = None


# class ImageModelsResponce(ImageBase):
#     description: str | None = None
#     photo: ImageBase | None = None
#     tags: List[ImageTagResponse] | None = None
#     created_date: Optional[datetime]
#     id: int

#     class Config:
#         from_attributes = True
