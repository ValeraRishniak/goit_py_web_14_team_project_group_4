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
from app.schemas.tags import ImageTagModel


async def get_my_photos(skip: int, limit: int, user: User, db: Session) -> List[Image]:
    """
    The get_my_photos function returns a list of images that belong to the user.

    :param skip: int: Skip the first x number of images
    :param limit: int: Limit the number of photos returned
    :param user: User: Pass the user object to the function
    :param db: Session: Access the database
    :return: A list of images that are owned by the user
    """
    
    return (
        db.query(Image).filter(Image.user_id == user.id).offset(skip).limit(limit).all()
    )


async def get_photo_by_id(photo_id: int, user: User, db: Session) -> Image:
    """
    The get_photo_by_id function returns a photo by its id.

    :param photo_id: int: Specify the id of the photo that we want to retrieve
    :param user: User: Ensure that the user is authenticated and has access to the photo
    :param db: Session: Pass the database session to the function
    :return: A photo by its id
    """

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
    """
    The create_photo function creates a new photo in the database.

    :param title: str: Set the title of the image
    :param description: str: Store the description of the image
    :param tags: str: Get the tags from the request body
    :param file: UploadFile: Pass the image file to the cloudinary uploader
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user who is logged in
    :return: A image object
    """

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


async def update_description(
    photo_id: int, title: str, description: str, tags: str, user: User, db: Session
) -> Image | None:
    """
    The update_description function updates the title, description or tags of a photo.

    :param photo_id: int: Identify which photo to update
    :param title: str: Update the title of a photo
    :param description: str: Update the description of an image
    :param tags: str: Get the tags from the request body
    :param user: User: Check if the user is the owner of the photo
    :param db: Session: Access the database
    :return: The photo object if the update was successful, none otherwise
    """

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


async def remove_photo(photo_id: int, user: User, db: Session) -> Image | None:
    """
    The remove_photo function removes a photo from the database and cloudinary.

    :param photo_id: int: Specify the id of the photo to be deleted
    :param user: User: Check if the user is authorized to delete the photo
    :param db: Session: Access the database
    :return: The photo object that was deleted
    """

    photo = db.query(Image).filter(Image.id == photo_id).first()

    if photo:
        if photo.user_id == user.id:
            config_cloudinary()
            cloudinary.uploader.destroy(photo.public_id)
            db.delete(photo)
            db.commit()
    return photo