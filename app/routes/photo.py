from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.photo_tags import  TagPhoto, TagPhotoResponse, PhotoBase, PhotoMoedels
from app.repository import photo as repository_photo

from app.repository.users import User
from app.services.auth import auth_service


router = APIRouter(prefix='/photos', tags=["photos"])


@router.get("/", response_model=List[PhotoMoedels])
async def see_potos(skip: int = 0, limit: int = 25, db: Session = Depends(get_db),  current_user: User = Depends(auth_service.get_current_user)):
    photos = await repository_photo.get_photos(skip, limit, current_user, db)
    return photos


@router.get("/{photo_id}", response_model=PhotoMoedels)
async def see_photo(photo_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    photo = await repository_photo.get_photo(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="By id not found photo")
    return photo


@router.post("/", response_model=PhotoMoedels, status_code= status.HTTP_201_CREATED)
async def create_contact(body: PhotoMoedels, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user) ):
    return await repository_photo.add_photo(body, current_user, db)

@router.put("/{photo_id}", response_model=PhotoMoedels)
async def update_description(body: PhotoMoedels, photo_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    photo = await repository_photo.update_description(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo by id is  not found")
    return photo

@router.delete("/{photo_id}", response_model=PhotoMoedels)
async def remove_photo(photo_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    photo = await repository_photo.remove_photo(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo

 
