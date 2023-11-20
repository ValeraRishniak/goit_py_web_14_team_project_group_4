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

router = APIRouter(prefix="/comments", tags=["comments"])

#Користувачі можуть коментувати світлини один одного:

# done - its work
@router.post("/", response_model=List[CommentResponse], status_code=status.HTTP_201_CREATED)
async def create_comment( image_id: int,
                          body: CommentBase, 
                          db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_comment.create_comment(image_id, body, db, current_user)

    return comment

# підключити ролі
#Done - its work
@router.put("/edit/{comment_id}", response_model=CommentUpdateResponse, 
            #dependencies=[Depends(allowed_update_comments)]
            )
async def edit_comment(comment_id: int, body: CommentBase, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    edited_comment = await repository_comment.edit_comment(comment_id, body, db, current_user)
    if edited_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="COMMENT NOT FOUND")
    return edited_comment


# підключити ролі
@router.delete("/delete/{comment_id}", response_model=CommentResponse,  # dependencies=[Depends(allowed_remove_comments)]
               )
async def delete_comment(comment_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    deleted_comment = await repository_comment.delete_comment(comment_id, db, current_user)
    if deleted_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='COMMENT NOT FOUND')
    return deleted_comment

# підключити ролі
@router.get("/single comment/{comment_id}", response_model=CommentResponse, #dependencies=[Depends(allowed_get_comments)]
            )
async def single_comment(comment_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_comment.show_single_comment(comment_id, db, current_user)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='COMMENT NOT FOUND')
    return comment

# підключити ролі
@router.get("/user comments/{user_id}", response_model=List[CommentResponse], #dependencies=[Depends(allowed_get_comments)]
            )
async def by_user_comments(user_id: int, db: Session = Depends(get_db),
                           current_user: User = Depends(auth_service.get_current_user)):
    comments = await repository_comment.show_my_comments(user_id, db)
    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='COMMENT NOT FOUND')
    return comments

# підключити ролі
@router.get("/foto_by_author/{user_id}/{foto_id}", response_model=List[CommentResponse],
            # dependencies=[Depends(allowed_get_comments)]
            )
async def by_user_foto_comments(user_id: int, image_id: int, db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    comments = await repository_comment.show_user_foto_comments(user_id, image_id, db)
    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='COMMENT NOT FOUND')
    return comments

