from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, or_, select

from app.database.models import ImageComment, User, Image

from app.schemas.comment import  CommentBase, CommentList
 
 
async def create_comment(db: Session, body: CommentBase,  image_id: int ):
    db_comment = ImageComment ( comment_description=body.comment_description, image_id=image_id )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

async def get_comment(db: Session, comment_id:int ):
    db_comment = db.get(ImageComment,comment_id)
    if db_comment:
      return db_comment

async def update_comment(db: Session, comment_id:int, comment_new: CommentBase ):
    db_comment = db.get(ImageComment,comment_id)
    if db_comment:
        try:
            db_comment.comment_description = comment_new
            await db.commit()
            await db.refresh(db_comment)
            return db_comment
        except Exception as e:
            await db.rollback()
            raise e
    return None

async def delete_comment(comment_id: int, db: Session):
    db_comment = await db.get(ImageComment, comment_id)
    if db_comment:
        try:
            await db.delete(db_comment)
            await db.commit()
            return db_comment
        except Exception as e:
            await db.rollback()
            raise e
        

async def get_photo_comments(offset: int, limit: int, image_id: int, db: Session):
    photo_comments = (select(ImageComment).filter(ImageComment.image_id == image_id).offset(offset).limit(limit))
    comments = await db.execute(photo_comments)
    result = comments.scalars().all()
    return result


async def get_user_comments(offset: int, limit: int, user_id: int, db: Session):
    user_comments = select(ImageComment).filter(ImageComment.user_id == user_id).offset(offset).limit(limit)
    comments = await db.execute(user_comments)
    result = comments.scalars().all()
    return result
