from typing import List
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, or_, select
import cloudinary 
import cloudinary.uploader



from app.database.models import   User, Image

from app.schemas.photo_tags import  PhotoModels, PhotoBase
          

# result = cloudinary.uploader.upload("https://upload.wikimedia.org/wikipedia/commons/a/ae/Olympic_flag.jpg", public_id = "olympic_flag")
# url = result.get('url')
# https://console.cloudinary.com/console/c-d8a03b96ed427346604eac79aeea58/media_library/homepage/asset/e6cfb21987e391a9c999f7a8fd6ddc51/manage?context=manage

async def get_photo_url(photo_id: int, user: User, db: Session):
    photo = db.query(Image).filter_by(and_(Image.id == photo_id, Image.user_id == user.id)).first()
    url = photo.url
    return url





