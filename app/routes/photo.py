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
    Request,
    status,
    File,
    UploadFile,
    Form,
)
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.schemas.photo_tags import (
    ImageTagModel,
    ImageTagResponse,
    PhotoBase,
    PhotoModels,
)
from app.repository import photo as repository_photo
from app.repository import photo_Cloudinary as repository_photo_cloudinary

from app.repository.users import User
from app.services.auth import auth_service
from app.schemas.photos import ImageResponse


router = APIRouter(prefix="/photos", tags=["photos"])


@router.get("/", response_model=List[PhotoModels])
async def see_potos(
    skip: int = 0,
    limit: int = 25,
    db: Session = Depends(get_db),
    # current_user: User = Depends(auth_service.get_current_user)
):
    photos = await repository_photo.get_photos(skip, limit, db)  # current_user,
    return photos


@router.get("/{photo_id}", response_model=PhotoModels)
async def see_photo(
    photo_id: int,
    db: Session = Depends(
        get_db
    ),  # current_user: User = Depends(auth_service.get_current_user)
):
    photo = await repository_photo.get_photo(photo_id, db)  #  current_user,
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="By id not found photo"
        )
    return photo


# @router.post("/ {photo_new}", response_model=PhotoModels, status_code= status.HTTP_201_CREATED)
# async def create_photo( name: str,  file: UploadFile=File(...), db: Session=Depends(get_db),
#                        # current_user: User = Depends(auth_service.get_current_user)
#                        ):
#     config_cloudinary()
#     result = cloudinary.uploader.upload(file.file)
#     url = result.get("url")

#     new_photo = await repository_photo.create_photo(name, db,  url )

#     return new_photo

"""
variant VRishniak
"""


@router.post("/new/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def create_foto(
    request: Request,
    title: str = Form(),
    description: str = Form(),
    tags: List = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_photo.create_photo(
        request, title, description, tags, file, db, current_user
    )


@router.put("/{photo_id}", response_model=PhotoModels)
async def update_description(
    body: PhotoModels,
    photo_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(auth_service.get_current_user)
):
    photo = await repository_photo.update_description(
        photo_id, body, db  # current_user,
    )
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo by id is  not found"
        )
    return photo


@router.delete("/{photo_id}", response_model=PhotoModels)
async def remove_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    #  current_user: User = Depends(auth_service.get_current_user)
):
    photo = await repository_photo.remove_photo(photo_id, db)  # current_user,
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    return photo


# @router.post("/{add_photo_cloudinary}", response_model=PhotoModels, status_code= status.HTTP_201_CREATED)
# async def add_photo(file: UploadFile=File(...),
#                     db: Session = Depends(get_db),
#                     name= str,
#                     description = str ,
#                     tags=  List[str]  ,
#                     #current_user: User = Depends(auth_service.get_current_user),
#                     width: int | None = Form( None, description="The desired width for the photo transformation (integer)")  ,
#                     height: int | None = Form( None, description="The desired height for the photo transformation (integer)") ,
#                     crop_mode: CropMode = Form( None, description="The cropping mode for the photo transformation (string)") ,
#                     rounding: int | None = Form( None, description="Rounding photo corners (in pixels)") ,
#                     background_color: BGColor = Form( None, description="The background color for the photo transformation (string)") ,
#                     rotation_angle: int | None = Form( None, description="The angle for the photo transformation (integer)") ,
#                     ):

#     if crop_mode is not None:
#         crop_mode = crop_mode.name
#     else:
#         crop_mode = None

#     if background_color is not None:
#         background_color = background_color.name
#     else:
#         background_color = "transparent"

#     # uploading a new photo
#     new_photo = await repository_photo_cloudinary.add_photo( file, description, tags, db,  width,  height, crop_mode, rounding, background_color,  rotation_angle,
#                                                                 # current_user,
#                                                             )

#     response = PhotoModels(
#         id=new_photo.id,
#         name=name,
#         description=new_photo.description,
#         created_date=new_photo.created_at,
#         tags= tags,
#         )
#     if new_photo:
#         return response


@router.post(
    "/make_QR/",
    status_code=status.HTTP_200_OK,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def make_URL_QR(
    photo_id: int,
    # current_user: User = Depends(auth_service.get_authenticated_user),
    db: Session = Depends(get_db),
):
    data = await repository_photo_cloudinary.get_URL_QR(photo_id, db)
    return data
