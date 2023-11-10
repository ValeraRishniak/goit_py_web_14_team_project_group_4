from typing import List
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, or_, select

from app.database.models import   User, Image
from app.schemas.photo_tags import  PhotoMoedels, PhotoBase


async def get_photos(  skip: int, limit: int,user: User, db: Session) -> List[Image]:
    return db.query(Image).offset(skip).limit(limit).filter(Image.user_id == user.id).all()

    

async def get_photo(photo_id: int, user: User, db: Session):
    contact = db.query(Image).filter_by(and_(Image.id == photo_id, Image.user_id == user.id)).first()
    return contact



async def add_photo(body: PhotoMoedels, user: User, db: Session) -> Image:
    photo = Image( description=body.description, image=body.photo,  tags=body.tags, user_id=user.id)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


async def update_description( photo_id: int, body: PhotoMoedels, user: User, db: Session) -> Image | None:
    photo = db.query(Image).filter(and_(Image.id==photo_id,  Image.user_id == user.id)).first()
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
