from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status, Path 
from fastapi_limiter.depends import RateLimiter


from app.database.db import get_db
from app.schemas.comment import  CommentBase, CommentList
from app.repository import comment as repository_comment
from app.repository.users import User
from app.services.auth import auth_service
from app.database.models import Role, User

router = APIRouter(prefix="/comments", tags=["comments"])

#Користувачі можуть коментувати світлини один одного:
@router.post("/", response_model=CommentList)
async def create_comment( image_id: int, body: CommentBase, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_comment.create_comment( body, current_user, db, image_id)

    return comment

@router.get("/{comment_id}", response_model=CommentList)
async def get_comment(comment_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_comment.get_comment(comment_id, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment for photo not found")
    return comment

@router.put("/update", response_model=CommentList)
async def update_comment(comment_id: int, body: CommentBase, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_comment.update_comment( body, comment_id, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment  not found")
#Чи є користувач власником коментаря, щоб його змінити    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only edit your own comments")
    
    updated_comment = await repository_comment.update_comment(body, comment_id, current_user, db)
    return updated_comment  

 
@router.delete("/delete", response_model=CommentList)
async def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_comment.delete_comment(comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Чи користувач є власником коментаря або адміністратор/модератор
    if comment.user_id != current_user.id and current_user.role not in [Role.moder, Role.admin]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own comments")

    await repository_comment.delete_comment(comment_id, db)
    print ('Delete comment ok') 

@router.get("/comments/{photo_id}", response_model=CommentList)
async def get_photo_comments(image_id: int, limit: int = 0, offset: int = 10, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    photo_comments = await repository_comment.get_photo_comments(limit,offset,image_id,db)
    return {'this photo contains the following comments': photo_comments} 

@router.get("/comments/{user_id}", response_model=CommentList)
async def get_user_comments(user_id: int, limit: int = 0, offset: int = 10, db: Session = Depends(get_db), 
                            current_user: User = Depends(auth_service.get_current_user)):
    comments_from_user = await repository_comment.get_user_comments(limit, offset, user_id, db)
    return {"this user left such comments": comments_from_user}