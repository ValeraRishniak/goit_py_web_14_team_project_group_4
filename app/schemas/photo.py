"""
variant VRishniak
"""

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field




class ImageModel(BaseModel):
    image_url: str = Field(max_length=300, default=None)
    title: str = Field(max_length=45)
    description: str = Field(max_length=255)
    tags: List[str] = []


class ImageModelsResponce(ImageModel):
    id: int
    avg_rating: Optional[float] = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ImageDescriptionUpdate(BaseModel):
    title: str = Field(max_length=45)
    description: str = Field(max_length=255)
    tags: List[str] = []



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
