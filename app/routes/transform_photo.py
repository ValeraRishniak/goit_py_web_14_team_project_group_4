from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import User
from app.schemas.photo import ImageModelsResponse
from app.services.auth import auth_service
from app.schemas.transform import TransformBodyModel
from app.repository import transform_photo

router = APIRouter(prefix="/transformations", tags=["transformations"])


@router.patch(
    "/{photo_id}", response_model=ImageModelsResponse, status_code=status.HTTP_200_OK
)
async def transform_method(
    photo_id: int,
    body: TransformBodyModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    photo = await transform_photo.transform_method(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    return photo


@router.post("/qr/{photo_id}", status_code=status.HTTP_201_CREATED)
async def show_qr(
    photo_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    photo = await transform_photo.show_qr(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    return StreamingResponse(photo, status_code=201, media_type="image/png")
