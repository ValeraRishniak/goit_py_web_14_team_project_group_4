from typing import List

from sqlalchemy.orm import Session

from app.database.models import ImageTag
from app.schemas.tags import ImageTagModel


async def get_tags(skip: int, limit: int, db: Session) -> List[ImageTag]:
    """
    The get_tags function returns a list of ImageTag objects.

    :param skip: int: Skip the first n tags
    :param limit: int: Limit the number of results returned
    :param db: Session: Pass the database session to the function
    :return: A list of ImageTag objects
    """
    
    return db.query(ImageTag).offset(skip).limit(limit).all()


async def get_tag_by_id(tag_id: int, db: Session) -> ImageTag:
    """
    The get_tag_by_id function returns the ImageTag object with the given tag_id.

    :param tag_id: int: Specify the id of the tag to be retrieved
    :param db: Session: Pass the database session to the function
    :return: A single ImageTag object
    """

    return db.query(ImageTag).filter(ImageTag.id == tag_id).first()


async def get_tags_by_list_values(
    values: List[ImageTagModel], db: Session
) -> List[ImageTag]:
    """
    The get_tags_by_list_values function takes a list of ImageTagModel objects and returns a list of ImageTag objects.

    :param values: List[ImageTagModel]: Pass in a list of ImageTagModel objects
    :param db: Session: Pass the database session to the function
    :return: A list of ImageTag objects
    """

    return (
        db.query(ImageTag)
        .filter(ImageTag.tag_name.in_([value.tag_name for value in values]))
        .all()
    )


async def create_tag(values: List[ImageTagModel], db: Session) -> ImageTag:
    """
    The create_tag function takes a list of ImageTagModel objects and a database session.

    :param values: List[ImageTagModel]: Pass the list of tags to be created
    :param db: Session: Pass the database session to the function
    :return: A list of ImageTag objects
    """

    bd_tags = await get_tags_by_list_values(values, db)
    for value in values:
        if not any([tag.tag_name == value.tag_name for tag in bd_tags]):
            new_tag = ImageTag(tag_name=value.tag_name)
            db.add(new_tag)
            db.commit()
            db.refresh(new_tag)
    return await get_tags_by_list_values(values, db)


async def update_tag(tag_id: int, body: ImageTagModel, db: Session) -> ImageTag | None:
    """
    The update_tag function updates an existing tag in the database.

    :param tag_id: int: Identify the tag to update
    :param body: ImageTagModel: Get the tag_name from the request body
    :param db: Session: Access the database
    :return: The updated tag
    """

    tag = await get_tag_by_id(tag_id, db)
    if tag:
        tag.tag_name = body.tag_name
        db.commit()
        db.refresh(tag)
    return tag


async def remove_tag(tag_id: int, db: Session) -> ImageTag | None:
    """
    The remove_tag function removes a tag from the database.

    :param tag_id: int: Specify the id of the tag to be removed
    :param db: Session: Pass the database session to the function
    :return: The tag that was deleted, or none if no such tag existed
    """

    tag = await get_tag_by_id(tag_id, db)
    if tag:
        db.delete(tag)
        db.commit()
    return tag
