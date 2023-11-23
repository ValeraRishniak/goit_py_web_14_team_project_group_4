from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import User
from app.schemas.tags import ImageTagModel, ImageTagResponse
from app.repository import tags as repository_tags
from app.services.auth import auth_service

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/all_tags/", response_model=List[ImageTagResponse])
async def read_tags(
    skip: int = 0,
    limit: int = 25,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The read_tags function returns a list of tags.
    
    :param skip: int: Skip the first n tags in the database
    :param limit: int: Limit the number of tags returned
    :param current_user: User: Get the current user from the request
    :param db: Session: Pass the database session to the repository layer
    :return: A list of tags
    """

    return await repository_tags.get_tags(skip, limit, db)


@router.get("/get_tag_by_id/{tag_id}", response_model=ImageTagResponse)
async def read_tag(
    tag_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The read_tag function returns a single tag by its ID.
    
    :param tag_id: int: Get the tag id from the url
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: A tag object
    """

    tag = await repository_tags.get_tag_by_id(tag_id, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.post(
    "/", response_model=List[ImageTagResponse], status_code=status.HTTP_201_CREATED
)
async def create_tag(
    tags: List[ImageTagModel],
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The create_tag function creates a new tag in the database.
        
    
    :param tags: List[ImageTagModel]: Pass in a list of tags to create
    :param current_user: User: Get the user that is currently logged in
    :param db: Session: Pass the database session to the repository layer
    :return: A list of imagetagmodel objects
    """

    return await repository_tags.create_tag(tags, db)


@router.put("/{tag_id}", response_model=ImageTagResponse)
async def update_tag(
    body: ImageTagModel,
    tag_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    
    """
    The update_tag function updates a tag in the database.
        The function takes an ImageTagModel object, which is used to update the tag's name and description.
        It also takes a tag_id, which is used to find the correct tag in the database.
        Finally it takes current_user and db as dependencies.

    :param body: ImageTagModel: Get the data from the request body
    :param tag_id: int: Identify the tag to be updated
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Pass the database session to the repository layer
    :return: A tag object
    """

    tag = await repository_tags.update_tag(tag_id, body, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.delete("/{tag_id}", response_model=ImageTagResponse)
async def remove_tag(
    tag_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The remove_tag function removes a tag from the database.
        Args:
            tag_id (int): The id of the tag to be removed.
            current_user (User): The user who is making this request.
            db (Session): A connection to the database, provided by FastAPI's dependency injection system.

    :param tag_id: int: Specify the tag that will be removed
    :param current_user: User: Check if the user is authenticated
    :param db: Session: Pass the database session to the repository layer
    :return: The removed tag
    """
    
    tag = await repository_tags.remove_tag(tag_id, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag
