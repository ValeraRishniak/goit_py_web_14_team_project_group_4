from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.database.models import Image, ImageComment, User
from app.schemas.comment import CommentBase


async def create_comment(
    image_id: int, body: CommentBase, user: User, db: Session
) -> ImageComment:
    """
    The create_comment function creates a new comment for an image.

    :param image_id: int: Get the image that is being commented on
    :param body: CommentBase: Get the comment_description from the request body
    :param user: User: Get the user id from the database
    :param db: Session: Create a database session
    :return: A list of comments
    """
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


async def edit_comment(
    comment_id: int, body: CommentBase, db: Session, user: User
) -> ImageComment | None:
    """
    The edit_comment function allows a user to edit their own comment.

    :param comment_id: int: Find the comment in the database
    :param body: CommentBase: Pass the data to update the comment
    :param db: Session: Access the database
    :param user: User: Check if the user is authorized to edit the comment
    :return: The updated comment or none if the comment with the specified id was not found
    """
    comment = db.query(ImageComment).filter(ImageComment.id == comment_id).first()
    if comment:
        # додати перевірку ролей
        if comment.user_id == user.id:
            comment.comment_description = body.comment_description
            comment.updated_at = func.now()
            comment.update_status = True
            db.commit()
    return comment


async def delete_comment(comment_id: int, db: Session, user: User) -> None:
    """
    The delete_comment function deletes a comment from the database.

    :param comment_id: int: Specify the id of the comment to be deleted
    :param db: Session: Pass a database session to the function
    :param user: User: Check if the user is authorized to delete a comment
    :return: A comment
    """
    comment = db.query(ImageComment).filter(ImageComment.id == comment_id).first()
    if comment:  # додати перевірку ролей
        db.delete(comment)
        db.commit()
    return comment


async def show_single_comment(
    comment_id: int, db: Session, user: User
) -> ImageComment | None:
    """
    The show_single_comment function returns a single comment from the database.

    :param comment_id: int: Identify the comment that is being requested
    :param db: Session: Pass the database session to the function
    :param user: User: Check if the user is authorized to view the comment
    :return: An ImageComment object or none
    """
    return (
        db.query(ImageComment)
        .filter(and_(ImageComment.id == comment_id, ImageComment.user_id == user.id))
        .first()
    )


async def show_my_comments(
    user_id: int, image_id: int, db: Session
) -> List[ImageComment] | None:
    """
    The show_my_comments function returns a list of comments made by the user on an image.

    :param user_id: int: Filter the comments by user_id
    :param image_id: int: Filter the comments by image_id
    :param db: Session: Pass in the database session, which is used to query the database
    :return: A list of ImageComment objects
    """
    return (
        db.query(ImageComment)
        .filter(
            and_(ImageComment.image_id == image_id, ImageComment.user_id == user_id)
        )
        .all()
    )


async def show_user_photo_comments(
    user_id: int, image_id: int, db: Session
) -> List[ImageComment] | None:
    """
    The show_user_photo_comments function returns a list of comments for a given user's photo.

    :param user_id: int: Specify the user id of the user whose comments are being requested
    :param image_id: int: Filter the comments by image_id
    :param db: Session: Connect to the database
    :return: A list of ImageComment objects
    """
    return (
        db.query(ImageComment)
        .filter(
            and_(ImageComment.image_id == image_id, ImageComment.user_id == user_id)
        )
        .all()
    )
