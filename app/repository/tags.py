from typing import List

from sqlalchemy.orm import Session

from app.database.models import ImageTag
from app.schemas.schemas import ImageTagModel


async def get_tags(skip: int, limit: int, db: Session) -> List[ImageTag]:
    return db.query(ImageTag).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, db: Session) -> ImageTag:
    return db.query(ImageTag).filter(ImageTag.id == tag_id).first()


async def create_tag(body: ImageTagModel, db: Session) -> ImageTag:
    tag = ImageTag(tag_name=body.tag_name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: ImageTagModel, db: Session) -> ImageTag | None:
    tag = db.query(ImageTag).filter(ImageTag.id == tag_id).first()
    if tag:
        tag.tag_name = body.tag_name
        db.commit()
    return tag


async def remove_tag(tag_id: int, db: Session) -> ImageTag | None:
    tag = db.query(ImageTag).filter(ImageTag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag
