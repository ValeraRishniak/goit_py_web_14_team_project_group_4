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


@router.get(
    "/my_photos",
    response_model=List[ImageWithCommentModelsResponse],
    dependencies=[Depends(access_get)],
)
async def see_my_photos(
    skip: int = 0,
    limit: int = 25,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The see_my_photos function returns a list of photos that the current user has uploaded.
    
    :param skip: int: Skip the first n photos
    :param limit: int: Limit the number of photos returned
    :param current_user: User: Get the current user from the database
    :param db: Session: Access the database
    :return: A list of photos
    """

    photos = await repository_photo.get_my_photos(skip, limit, current_user, db)
    if photos is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Your photo not found"
        )
    return photos


@router.get(
    "/by_id/{photo_id}",
    response_model=ImageModelsResponse,
    dependencies=[Depends(access_get)],
)
async def see_one_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The see_one_photo function returns a single photo by id.
        Args:
            photo_id (int): The id of the photo to be returned.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): User object with user information from auth token payload. Defaults to Depends(auth_service.get_current_user).
    
    :param photo_id: int: Get the id of the photo to be viewed
    :param db: Session: Pass a database session to the function
    :param current_user: User: Get the current user
    :return: A photo object
     """
    
    photo = await repository_photo.get_photo_by_id(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found your photo by id"
        )
    return photo


@router.post(
    "/new/",
    response_model=ImageModelsResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(access_create)],
)
async def create_photo(
    title: str = Form(),
    description: str = Form(),
    tags: str = Form(None),
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_photo function creates a new photo in the database.
        The function takes in a title, description, tags (optional), and file.
        It then uses the repository_photo module to create the photo.
    
    :param title: str: Get the title of the photo from the form
    :param description: str: Store the description of the photo
    :param tags: str: Pass the tags to the create_photo function
    :param file: UploadFile: Get the file from the request
    :param db: Session: Get the database session
    :param current_user: User: Get the user that is currently logged in
    :return: A tuple of the photo object and a list of tag objects
    """

    return await repository_photo.create_photo(
        title, description, tags, file, db, current_user
    )


@router.put(
    "/{photo_id}",
    response_model=ImageModelsResponse,
    dependencies=[Depends(access_update)],
)
async def update_description(
    photo_id: int,
    title: str = Form(None),
    description: str = Form(None),
    tags: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_description function updates the description of a photo.
        The function takes in an integer representing the id of a photo, and three strings representing
        title, description and tags respectively. It also takes in two dependencies: db (a database session) 
        and current_user (the user who is currently logged into the application).
    
    :param photo_id: int: Find the photo in the database
    :param title: str: Update the title of a photo
    :param description: str: Update the description of a photo
    :param tags: str: Update the tags of a photo
    :param db: Session: Pass a database session to the function
    :param current_user: User: Check if the user is authenticated
    :return: The photo object
    """

    photo = await repository_photo.update_description(
        photo_id, title, description, tags, current_user, db
    )
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your photo by id is not found",
        )
    return photo


@router.delete(
    "/{photo_id}",
    response_model=ImageModelsResponse,
    dependencies=[Depends(access_delete)],
)
async def remove_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The remove_photo function removes a photo from the database.
        Args:
            photo_id (int): The id of the photo to be removed.
            db (Session, optional): A database session object for interacting with the database. Defaults to Depends(get_db).
            current_user (User, optional): The user currently logged in and making this request. Defaults to Depends(auth_service.get_current_user).
    
    :param photo_id: int: Get the photo id from the url
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A photo object
    """
    
    photo = await repository_photo.remove_photo(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Your photo not found"
        )
    return photo
