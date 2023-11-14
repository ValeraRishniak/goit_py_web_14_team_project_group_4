from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, or_, select

from app.database.models import ImageComment

from app.schemas.comment import  CommentBase
 
 
async def create_comment(db: Session, comment_id:int, comment: CommentBase ):
    db_comment = ImageComment(id=comment_id,**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# async def create_comment(db: Session, comment_id:int, comment: CommentBase ):
#     db_comment = ImageComment(id=comment_id,**comment.dict())
#     db.add(db_comment)
#     db.commit()
#     db.refresh(db_comment)
#     return db_comment

# async def create_comment(db: Session, comment_id:int, comment: CommentBase ):
#     db_comment = ImageComment(id=comment_id,**comment.dict())
#     db.add(db_comment)
#     db.commit()
#     db.refresh(db_comment)
#     return db_comment

