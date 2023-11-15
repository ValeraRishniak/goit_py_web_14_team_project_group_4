from typing import List
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, or_, select
from fastapi import File

from app.database.models import config_cloudinary
import cloudinary
import cloudinary.uploader
import shutil


from app.database.models import   User, Image

from app.schemas.photo_tags import  PhotoModels, PhotoBase



async def get_photos(  skip: int, limit: int,user: User, db: Session) -> List[Image]:
    return db.query(Image).offset(skip).limit(limit).filter(Image.user_id == user.id).all()

    

async def get_photo(photo_id: int, user: User, db: Session):
    photo = db.query(Image).filter_by(and_(Image.id == photo_id, Image.user_id == user.id)).first()
    return photo




async def add_photo( photo:File(),
                #    user: User,
                    db: Session,
                    name: str | None = None,
                    description: str | None = None,
                    tags: List[str] | None = None,
                    ) -> Image:
    config_cloudinary()
    
    uploaded_file_info = cloudinary.uploader.upload(photo.file)

    photo_url = uploaded_file_info["secure_url"]
    # public_id = uploaded_file_info["public_id"]
    
    photo = Image(name=name, description=description, tags=tags, url=photo_url)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo



async def update_description( photo_id: int, body: PhotoModels, user: User, db: Session) -> Image | None:
    photo = db.query(Image).filter_by(id=photo_id).first()
    if photo:
        photo.description = body.description
        db.commit()
    return photo


async def remove_photo( photo_id: int, user: User, db: Session) -> Image | None:
    photo = db.query(Image).filter(and_(Image.id == photo_id, Image.user_id == user.id)).first()
    if photo:
        db.delete(photo)
        db.commit()
    return photo

async def create_photo( text:str, db:Session, url:str, 
                       #user: User
                         ):
    
    Photo_url = Image( description= text , url=url )
    db.add(Photo_url)
    db.commit()
    db.refresh(Photo_url)
    return Photo_url
