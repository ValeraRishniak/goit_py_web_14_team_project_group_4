import cloudinary
import cloudinary.uploader
from uuid import uuid4

from typing import List
from datetime import datetime
from pydantic_core import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import UploadFile


from app.conf.config import config_cloudinary
from app.database.models import User, Image
from app.repository.tags import create_tag
from app.schemas.photo import ImageModel
from app.schemas.tags import ImageTagModel


async def get_my_photos(skip: int, limit: int, user: User, db: Session) -> List[Image]:
    return (
        db.query(Image).filter(Image.user_id == user.id).offset(skip).limit(limit).all()
    )


async def get_photo_by_id(photo_id: int, user: User, db: Session) -> Image:
    photo = (
        db.query(Image)
        .filter(and_(Image.user_id == user.id, Image.id == photo_id))
        .first()
    )
    return photo


async def create_photo(
    title: str,
    description: str,
    tags: str,
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

    image = Image(
        image_url=url,
        title=title,
        description=description,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        done=True,
        user_id=current_user.id,
        public_id=public_id,
    )

    if tags:
        result = []
        tags = tags.split(",")
        for tag in tags:
            tag.strip()
            try:
                current_tag = ImageTagModel(tag_name=tag)
                result.append(current_tag)
            except ValidationError as e:
                print(e)
        image.tags = await create_tag(result, db)

    db.add(image)
    db.commit()
    db.refresh(image)

    return image


# додати роль
async def update_description(
    photo_id: int, title: str, description: str, tags: str, user: User, db: Session
) -> Image | None:
    photo = db.query(Image).filter(Image.id == photo_id).first()
    if photo:
        if photo.user_id == user.id:
            photo.title = title
            photo.description = description
            if tags:
                result = []
                tags = tags.split(",")
                for tag in tags:
                    tag.strip()
                    current_tag = ImageTagModel(tag_name=tag)
                    result.append(current_tag)
                photo.tags = await create_tag(result, db)
            db.commit()
    return photo


# додати роль
async def remove_photo(photo_id: int, user: User, db: Session) -> Image | None:
    photo = db.query(Image).filter(Image.id == photo_id).first()

    if photo:
        if photo.user_id == user.id:
            config_cloudinary()
            cloudinary.uploader.destroy(photo.public_id)
            db.delete(photo)
            db.commit()
    return photo
