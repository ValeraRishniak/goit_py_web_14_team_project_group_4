import cloudinary
import cloudinary.uploader
from uuid import uuid4

from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import Request, UploadFile


from app.conf.config import config_cloudinary
from app.database.models import User, Image
from app.repository.tags import get_tags
from app.schemas.photo import ImageDescriptionUpdate


# Було - не працювало
# async def get_photos(skip: int, limit: int, user: User, db: Session) -> List[Image]:
#     return db.query(Image).offset(skip).limit(limit).filter(Image.user_id == user.id).all()


# Стало - працює
async def get_photos(skip: int, limit: int, user: User, db: Session) -> List[Image]:
    return (
        db.query(Image).offset(skip).limit(limit).filter(Image.user_id == user.id).all()
    )


# Додав нову функцію


async def get_my_photos(skip: int, limit: int, user: User, db: Session) -> List[Image]:
    return (
        db.query(Image).filter(Image.user_id == user.id).offset(skip).limit(limit).all()
    )


# Було - не працювало
# async def get_photo(photo_id: int, db: Session,  user: User):
#     photo = db.query(Image).filter_by(and_(Image.id == photo_id, Image.user_id == user.id)).first()
#     return photo


# стало - працює
async def get_photo_by_id(photo_id: int, user: User, db: Session) -> Image:
    photo = (
        db.query(Image)
        .filter(and_(Image.user_id == user.id, Image.id == photo_id))
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
    public_id = f"PhotoShake/{uuid4().hex}"

    config_cloudinary()
    cloudinary.uploader.upload(file.file, public_id=public_id)
    url = cloudinary.CloudinaryImage(public_id).build_url(
        width=500, height=500, crop="fill"
    )

    if tags:
        tags = get_tags(tags[0].split(","), current_user, db)

    photo = Image(
        image_url=url,
        title=title,
        description=description,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        # tags=tags,
        done=True,
        user_id=current_user.id,
        public_id=public_id,
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return photo


# додати роль
# не працюють теги, якщо у свагері робити зміни, не змінюючи тегів, title i description працюють
async def update_description(
    photo_id: int, body: ImageDescriptionUpdate, user: User, db: Session
) -> Image | None:
    photo = db.query(Image).filter(Image.id == photo_id).first()
    if photo:
        if photo.user_id == user.id:
            photo.title = body.title
            photo.description = body.description
            photo.tags = body.tags
            db.commit()
    return photo


# додати роль
# додати в ствроення фотографії (в модель і функцію параметр public_id, оскільки по ньому здійснюється видалення фото з cloudinary)
# поки не буде працювати
async def remove_photo(photo_id: int, user: User, db: Session) -> Image | None:
    photo = db.query(Image).filter(Image.id == photo_id).first()
    if photo:
        if photo.user_id == user.id:
            config_cloudinary()
            cloudinary.uploader.destroy(photo.public_id)
            db.delete(photo)
            db.commit()
    return photo
