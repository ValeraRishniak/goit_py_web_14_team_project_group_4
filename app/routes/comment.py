from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status, Path
from fastapi_limiter.depends import RateLimiter


from app.database.db import get_db
from app.schemas.comment import CommentBase, CommentResponse, CommentUpdateResponse
from app.repository import comment as repository_comment
from app.repository.users import User
from app.services.auth import auth_service
from app.database.models import Role, User
from app.services.roles import RoleChecker

router = APIRouter(prefix="/comments", tags=["comments"])

access_get = RoleChecker([Role.admin, Role.moderator, Role.user])
access_create = RoleChecker([Role.admin, Role.moderator, Role.user])
access_update = RoleChecker([Role.admin, Role.moderator, Role.user])
access_delete = RoleChecker([Role.admin, Role.moderator])


@router.post(
    "/{image_id}",
    response_model=List[CommentResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(access_create)],
)
async def create_comment(
    image_id: int,
    body: CommentBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_comment function creates a new comment for the image with the given ID.
        The user who created this comment is stored in the database as well.
    
    :param image_id: int: Specify the image that the comment is being made on
    :param body: CommentBase: Get the body of the comment
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user who is currently logged in
    :return: A comment object
    """

    return await repository_comment.create_comment(image_id, body, current_user, db)


@router.put(
    "/edit/{comment_id}",
    response_model=CommentUpdateResponse,
    dependencies=[Depends(access_update)],
)
async def edit_comment(
    comment_id: int,
    body: CommentBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The edit_comment function allows a user to edit their own comment.
        The function takes in the comment_id, body, db and current_user as parameters.
        It then calls the edit_comment function from repository/comment.py which returns an edited comment object if successful or None if not successful.
    
    :param comment_id: int: Identify the comment to edit
    :param body: CommentBase: Pass the new comment body to the function
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :return: A commentbase object, which is a pydantic model
    """

    edited_comment = await repository_comment.edit_comment(
        comment_id, body, db, current_user
    )
    if edited_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return edited_comment


@router.delete(
    "/delete/{comment_id}",
    response_model=CommentResponse,
    dependencies=[Depends(access_delete)],
)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The delete_comment function deletes a comment from the database.
        The function takes in an integer representing the id of the comment to be deleted,
        and returns a dictionary containing information about that comment.
    
    :param comment_id: int: Specify the comment to delete
    :param db: Session: Get the database session
    :param current_user: User: Get the user who is making the request
    :return: The deleted comment
    """

    deleted_comment = await repository_comment.delete_comment(
        comment_id, db, current_user
    )
    if deleted_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return deleted_comment


@router.get(
    "/single_comment/{comment_id}",
    response_model=CommentResponse,
    dependencies=[Depends(access_get)],
)
async def single_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The single_comment function returns a single comment from the database.
        The function takes in an integer, comment_id, and uses it to query the database for a single comment.
        If no such comment exists, then an HTTPException is raised with status code 404 and detail &quot;Comment not found&quot;.
        Otherwise, the function returns that single Comment object.
    
    :param comment_id: int: Get the comment_id from the url
    :param db: Session: Connect to the database
    :param current_user: User: Get the user who is currently logged in
    :return: A comment object
    """

    comment = await repository_comment.show_single_comment(comment_id, db, current_user)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return comment


@router.get(
    "/user_comments/{user_id}",
    response_model=List[CommentResponse],
    dependencies=[Depends(access_get)],
)
async def by_user_comments(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The by_user_comments function returns all comments made by a user.
        Args:
            user_id (int): The id of the user whose comments are being returned.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): User object for the currently logged in user. Defaults to Depends(auth_service.get_current_user).
    
    :param user_id: int: Pass the user_id of the user whose comments are to be retrieved
    :param db: Session: Get the database session
    :param current_user: User: Get the user_id of the current user
    :return: A list of comments
    """

    comments = await repository_comment.show_my_comments(user_id, db)
    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return comments


@router.get(
    "/photo_by_author/{user_id}/{photo_id}",
    response_model=List[CommentResponse],
    dependencies=[Depends(access_get)],
)
async def by_user_photo_comments(
    user_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The by_user_photo_comments function returns a list of comments for a specific user and photo.
        The function takes in the following parameters:
            - user_id: int, the id of the user whose comments are being returned.
            - image_id: int, the id of the image whose comments are being returned.
        The function returns a list containing all comment objects that match both parameters.
    
    :param user_id: int: Get the user_id of the user who commented on a photo
    :param image_id: int: Identify the photo that the comment is associated with
    :param db: Session: Get the database session
    :return: A list of comments
    """
    
    comments = await repository_comment.show_user_photo_comments(user_id, image_id, db)
    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return comments
