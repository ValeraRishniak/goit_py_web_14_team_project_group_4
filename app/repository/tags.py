from typing import List
from sqlalchemy import select

from sqlalchemy.orm import Session

from app.database.models import ImageTag
from app.schemas.tags import ImageTagModel



async def get_tags(skip: int, limit: int, db: Session) -> List[ImageTag]:
    return db.query(ImageTag).offset(skip).limit(limit).all()


async def get_tag_by_id(tag_id: int, db: Session) -> ImageTag:
    return db.query(ImageTag).filter(ImageTag.id == tag_id).first()


async def get_tags_by_list_values(
    values: list[ImageTagModel], db: Session
) -> List[ImageTag]:
    return (
        db.query(ImageTag)
        .filter(ImageTag.tag_name.in_([value.tag_name for value in values]))
        .all()
    )


async def create_tag(values: list[ImageTagModel], db: Session) -> ImageTag:
    bd_tags = await get_tags_by_list_values(values, db)
    for value in values:
        if not any([tag.tag_name == value.tag_name for tag in bd_tags]):
            new_tag = ImageTag(tag_name=value.tag_name)
            db.add(new_tag)
            db.commit()
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


async def get_tags_by_list_values(values: list[str], db: Session) -> list[ImageTag]:
    """
    The get_tags_by_list_values function takes a list of strings and an AsyncSession object as arguments.
    It returns a list of Tag objects that match the names in the values argument.

    :param values: list[str]: Pass in a list of strings to the function
    :param db: AsyncSession: Pass in the database session
    :return: A list of tag objects
    """
    tags = db.scalars(select(ImageTag)  # await
        .filter(ImageTag.tag_name.in_(values))
    )
    return tags.all()  # noqa


async def get_or_create_tags(values: list[str], db: Session) -> list[ImageTag]:
    """
    The get_or_create_tags function takes a list of strings and an async database session.
    It returns a list of Tag objects.
    If the tag already exists in the database, it is returned as-is. If not, it is created and then returned.

    :param values: list[str]: Pass in a list of strings
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of tag objects
    """
    tags = await get_tags_by_list_values(values, db)
    new_tags = []

    for value in values:
        for tag in tags:
            if value == tag.tag_name:
                break
        else:
            new_tags.append(ImageTag(tag_name=value.strip()))

    db.add_all(new_tags)

    db.commit()
    for new_tag in new_tags:
        db.refresh(new_tag)

    tags.extend(new_tags)

    return tags
