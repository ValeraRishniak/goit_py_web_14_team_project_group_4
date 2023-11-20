from typing import List

from sqlalchemy.orm import Session

from app.database.models import ImageTag
from app.schemas.tags import ImageTagModel



async def get_tags(skip: int, limit: int, db: Session) -> List[ImageTag]:
    return db.query(ImageTag).offset(skip).limit(limit).all()


async def get_tag_by_id(tag_id: int, db: Session) -> ImageTag:
    return db.query(ImageTag).filter(ImageTag.id == tag_id).first()


async def get_tags_by_list_values(
    values: List[ImageTagModel], db: Session
) -> List[ImageTag]:
    return (
        db.query(ImageTag)
        .filter(ImageTag.tag_name.in_([value.tag_name for value in values]))
        .all()
    )


async def create_tag(values: List[ImageTagModel], db: Session) -> ImageTag:
    bd_tags = await get_tags_by_list_values(values, db)
    for value in values:
        if not any([tag.tag_name == value.tag_name for tag in bd_tags]):
            new_tag = ImageTag(tag_name=value.tag_name)
            db.add(new_tag)
            db.commit()
            db.refresh(new_tag)
    return await get_tags_by_list_values(values, db)


async def update_tag(tag_id: int, body: ImageTagModel, db: Session) -> ImageTag | None:
    tag = await get_tag_by_id(tag_id, db)
    if tag:
        tag.tag_name = body.tag_name
        db.commit()
        db.refresh(tag)
    return tag


async def remove_tag(tag_id: int, db: Session) -> ImageTag | None:
    tag = await get_tag_by_id(tag_id, db)
    if tag:
        db.delete(tag)
        db.commit()
    return tag
