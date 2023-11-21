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
    comments = await repository_comment.show_user_photo_comments(user_id, image_id, db)
    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return comments
