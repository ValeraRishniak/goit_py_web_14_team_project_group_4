from typing import List
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, or_, select
from fastapi import File, Request, UploadFile

from app.conf.config import config_cloudinary
import cloudinary
import cloudinary.uploader
import shutil


from app.database.models import User, Image

from app.schemas.photo_tags import PhotoModels, PhotoBase
from app.repository.tags import get_tags


async def get_photos(skip: int, limit: int, user: User, db: Session) -> List[Image]:
    return (
        db.query(Image).offset(skip).limit(limit).filter(Image.user_id == user.id).all()
    )


async def get_photo(photo_id: int, user: User, db: Session):
    photo = (
        db.query(Image)
        .filter_by(and_(Image.id == photo_id, Image.user_id == user.id))
        .first()
    )
    return photo


# async def create_photo( text:str, db:Session, url:str,
#                        #user: User
#                          ):

#     Photo_url = Image( description= text , url=url )
#     db.add(Photo_url)
#     db.commit()
#     db.refresh(Photo_url)
#     return Photo_url

"""
variant VRishniak
"""


async def create_photo(
    request: Request,
    title: str,
    description: str,
    tags: List,
    file: UploadFile,
    db: Session,
    current_user: User,
) -> Image:
    photo_number = 1

    db_photo = (
        db.query(Image)
        .filter(and_(Image.user_id == current_user.id, Image.id == photo_number))
        .first()
    )

    if db_photo:
        photo_number += 1

    public_id = f"PhotoShake/{photo_number}"

    config_cloudinary()
    cloudinary.uploader.upload(file.file, public_id=public_id)
    url = cloudinary.CloudinaryImage(f"PhotoShake/{photo_number}").build_url(
        width=250, height=250, crop="fill"
    )
    url2 = url

    if tags:
        tags = get_tags(tags[0].split(","), current_user, db)

    foto = Image(
        image_url=url,
        transform_url=url2,
        title=title,
        description=description,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        # tags=tags,
        done=True,
        user_id=current_user.id,
    )
    db.add(foto)
    db.commit()
    db.refresh(foto)

    return foto


async def update_description(
    photo_id: int, body: PhotoModels, user: User, db: Session
) -> Image | None:
    photo = db.query(Image).filter_by(id=photo_id).first()
    if photo:
        photo.description = body.description
        db.commit()
    return photo


async def remove_photo(photo_id: int, user: User, db: Session) -> Image | None:
    photo = (
        db.query(Image)
        .filter(and_(Image.id == photo_id, Image.user_id == user.id))
        .first()
    )
    if photo:
        db.delete(photo)
        db.commit()
    return photo
