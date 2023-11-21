from typing import List
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

from app.schemas.photo import (
    ImageModel,
    ImageModelsResponse,
    ImageWithCommentModelsResponse,
)
from app.repository import photo as repository_photo
from app.repository.users import User
from app.services.auth import auth_service
from app.services.roles import RoleChecker
from app.database.models import Role


router = APIRouter(prefix="/photos", tags=["photos"])

access_get = RoleChecker([Role.admin, Role.moderator, Role.user])
access_create = RoleChecker([Role.admin, Role.moderator, Role.user])
access_update = RoleChecker([Role.admin, Role.moderator, Role.user])
access_delete = RoleChecker([Role.admin, Role.user])


@router.get("/my_photos", response_model=List[ImageWithCommentModelsResponse],
             dependencies=[Depends(access_get)]
             )

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


@router.get("/by_id/{photo_id}", response_model=ImageModelsResponse, 
            dependencies=[Depends(access_get)]
            )

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



@router.post("/new/", response_model=ImageModelsResponse, status_code=status.HTTP_201_CREATED,
              dependencies=[Depends(access_create)]
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


@router.put("/{photo_id}", response_model=ImageModelsResponse, 
            dependencies=[Depends(access_update)])
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


@router.delete("/{photo_id}", response_model=ImageModelsResponse, 
               dependencies=[Depends(access_delete)])
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

