from typing import List
import cloudinary
import cloudinary.uploader
import shutil

from app.database.models import config_cloudinary

from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.schemas.photo_tags import  ImageTagModel, ImageTagResponse, PhotoBase, PhotoModels
from app.repository import photo as repository_photo

from app.repository.users import User
from app.services.auth import auth_service


router = APIRouter(prefix='/photos', tags=["photos"])



@router.get("/", response_model=List[PhotoModels])
async def see_potos(skip: int = 0, limit: int = 25, db: Session = Depends(get_db),  
                     # current_user: User = Depends(auth_service.get_current_user)
                    ):
    photos = await repository_photo.get_photos(skip, limit, # current_user,
                                               db)
    return photos



@router.get("/{photo_id}", response_model=PhotoModels)
async def see_photo(photo_id: int, db: Session = Depends(get_db), #current_user: User = Depends(auth_service.get_current_user)
                    ):
    photo = await repository_photo.get_photo(photo_id, #  current_user, 
                                             db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="By id not found photo")
    return photo



@router.post("/", response_model=PhotoModels, status_code= status.HTTP_201_CREATED)
async def add_photo(file: UploadFile=File(...),  
                    db: Session = Depends(get_db), 
                    name=str,
                    description = str ,
                    tags =  List[str]  ,
                    #current_user: User = Depends(auth_service.get_current_user), 
                    ):
    # result = cloudinary.uploader.upload(file.file)
    # url = result.get("url")
    
    new_photo = await repository_photo.add_photo( #current_user,
                                                  name ,db, file, description, tags  )
    url = new_photo.url

    return new_photo, url
    # return await repository_photo.add_photo(body,  current_user,
    #                                         db, url),        

@router.post("/{photo_new}", response_model=PhotoModels, status_code= status.HTTP_201_CREATED)
async def create_photo( name: str, file: UploadFile=File(...), db: Session=Depends(get_db),
                       # current_user: User = Depends(auth_service.get_current_user)
                       ):
    config_cloudinary()
    result = cloudinary.uploader.upload(file.file, public_id = name)
    url = result.get("url")
 
    new_photo = await repository_photo.create_photo(file, db, name, url )
    
    return url, new_photo
                                       

@router.put("/{photo_id}", response_model=PhotoModels)
async def update_description(body: PhotoModels, photo_id: int, db: Session = Depends(get_db),
                         #current_user: User = Depends(auth_service.get_current_user)
                         ):
    photo = await repository_photo.update_description(photo_id, body, # current_user,
                                                      db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo by id is  not found")
    return photo


@router.delete("/{photo_id}", response_model=PhotoModels)
async def remove_photo(photo_id: int, db: Session = Depends(get_db),
                       #  current_user: User = Depends(auth_service.get_current_user)
                         ):
    photo = await repository_photo.remove_photo(photo_id, # current_user,
                                                db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo

 
