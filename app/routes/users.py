from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from app.database.db import get_db
from app.database.models import User
from app.repository import users as repository_users
from app.services.auth import auth_service
from app.conf.config import settings
from app.schemas.user import UserDb


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The read_users_me function returns the current user's information.
        ---
        get:
          tags: [users]
          summary: Returns the current user's information.
          responses:  # The possible responses that this endpoint can return, and their status codes.
            &quot;200&quot;:  # Status code 200 means OK!
              description: Successfully retrieved the current user's info!
    
    :param current_user: User: Get the user object from the database
    :param db: Session: Pass the database session to the function
    :return: A user object
    """
    user = await repository_users.get_me(current_user, db)
    return user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(
        file.file, public_id=f'PhotoSHAKE/{current_user.id}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'PhotoSHAKE/{current_user.id}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
