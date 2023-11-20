from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_, func 
from app.database.models import  Image, ImageComment, User

from app.schemas.comment import  CommentBase
 


async def create_comment(image_id: int, body: CommentBase, db: Session, user: User) -> ImageComment:
    image = db.query(Image).filter(Image.id == image_id).first()
    comment = ImageComment(
        comment_description=body.comment_description, user_id=user.id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    if not image.comment:
        image.comment = []
    image.comment.append(comment)
    db.commit()
    db.refresh(image)
    return [comment]



async def edit_comment(comment_id: int, body: CommentBase, db: Session, user: User) -> ImageComment | None:
    comment = db.query(ImageComment).filter(ImageComment.id == comment_id).first()
    if comment:
        #додати перевірку ролей
        if comment.user_id == user.id:
            comment.comment_description = body.comment_description
            comment.updated_at = func.now()
            comment.update_status = True
            db.commit()
    return comment


async def delete_comment(comment_id: int, db: Session, user: User) -> None:
    comment = db.query(ImageComment).filter(ImageComment.id == comment_id).first()
    if comment:  # додати перевірку ролей
        db.delete(comment)
        db.commit()
    return comment


async def show_single_comment(comment_id: int, db: Session, user: User) -> ImageComment | None:
    return db.query(ImageComment).filter(and_(ImageComment.id == comment_id, ImageComment.user_id == user.id)).first()


async def show_my_comments(user_id: int, image_id: int, db: Session) -> List[ImageComment] | None:
    return db.query(ImageComment).filter(and_(ImageComment.image_id == image_id, ImageComment.user_id == user_id)).all()


async def show_user_foto_comments(user_id: int, image_id: int, db: Session) -> List[ImageComment] | None:
    return db.query(ImageComment).filter(and_(ImageComment.image_id == image_id, ImageComment.user_id == user_id)).all()
