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
    """
    The transform_method function takes a photo_id and a TransformBodyModel object,
        which contains the following fields:
            - transform_type (str): The type of transformation to be applied. 
                Currently supported values are &quot;rotate&quot; and &quot;flip&quot;.
            - degrees (int): The number of degrees to rotate the image by. Only used if transform_type is set to &quot;rotate&quot;. 
                If not specified, defaults to 90. Must be one of 0, 90, 180 or 270. Any other value will result in an error response.&lt;/code&gt;
    
    :param photo_id: int: Get the photo from the database
    :param body: TransformBodyModel: Get the body of the request
    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :param : Get the photo_id from the url
    :return: The photo object
    """
    
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
    """
    The show_qr function returns a QR code for the photo with the given ID.
        The QR code is generated using the photo's URL and can be used to quickly access it.
        
    
    :param photo_id: int: Specify the photo that we want to get the qr code for
    :param current_user: User: Get the current user from the database
    :param db: Session: Get a database session
    :param : Get the photo_id from the url
    :return: A streamingresponse object
    """

    photo = await transform_photo.show_qr(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    return StreamingResponse(photo, status_code=201, media_type="image/png")
