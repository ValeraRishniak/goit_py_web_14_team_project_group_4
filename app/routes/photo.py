from typing import List
import cloudinary
import cloudinary.uploader
import shutil

from app.database.models import CropMode, BGColor
from app.conf.config import config_cloudinary

from fastapi_limiter.depends import RateLimiter
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    File,
    UploadFile,
    Form,
)
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.schemas.photo import ImageModel, ImageModelsResponse, ImageWithCommentModelsResponse
from app.repository import photo as repository_photo
from app.repository.users import User
from app.services.auth import auth_service


router = APIRouter(prefix="/photos", tags=["photos"])


@router.get("/my_photos", response_model=List[ImageWithCommentModelsResponse])
async def see_my_photos(
    skip: int = 0,
    limit: int = 25,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    photos = await repository_photo.get_my_photos(skip, limit, current_user, db)
    if photos is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Your photo not found"
        )
    return photos


@router.get("/by_id/{photo_id}", response_model=ImageModelsResponse)
async def see_one_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    photo = await repository_photo.get_photo_by_id(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found your photo by id"
        )
    return photo


@router.post(
    "/new/", response_model=ImageModelsResponse, status_code=status.HTTP_201_CREATED
)
async def create_foto(
    title: str = Form(),
    description: str = Form(),
    tags: str = Form(None),
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_photo.create_photo(
        title, description, tags, file, db, current_user
    )


@router.put("/{photo_id}", response_model=ImageModelsResponse)
async def update_description(
    body: ImageModel,
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    photo = await repository_photo.update_description(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your photo by id is not found",
        )
    return photo


@router.delete("/{photo_id}", response_model=ImageModelsResponse)
async def remove_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    photo = await repository_photo.remove_photo(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Your photo not found"
        )
    return photo

