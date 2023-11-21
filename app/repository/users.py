from typing import List
from libgravatar import Gravatar
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.models import Image, ImageComment, Role, User
from app.schemas.user import UserModel, UserProfileModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email.

    :param email: str: Specify the type of parameter that will be passed to the function
    :param db: Session: Pass the database session to the function
    :return: A user object
    """
    return db.query(User).filter(User.email == email).first()


async def get_me(user: User, db: Session):
<<<<<<< Updated upstream
    user = db.query(User).filter(User.id == user.id).first()
    return user
=======
    """
    The get_me function returns the user object of the currently logged in user.

    :param user: User: Pass the user object to the function
    :param db: Session: Access the database
    :return: A user object
    """
    return db.query(User).filter(User.id == user.id).first()
>>>>>>> Stashed changes


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.

    :param body: UserModel: Get the data from the request body
    :param db: Session: Access the database
    :return: A user object
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    new_user.role = Role.user
    result = db.execute(select(User))
    userscount = len(result.all())
    if not userscount:
        new_user.role = Role.admin
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user in the database
    :param token: str | None: Update the refresh_token field in the user table
    :param db: Session: Commit the changes to the database
    :return: None
    """
    user.refresh_token = token
    db.commit()


<<<<<<< Updated upstream
async def update_user_inform(email:str, 
                             username:str|None, 
                             password:str|None,
                             db: Session) -> User:
    user =  db.query(User).filter_by(email=email).first()
=======
async def update_user_inform(
    email: str, username: str | None, password: str | None, db: Session
) -> User:
    """
    The update_user_inform function updates the user's information in the database.

    :param email: str: Identify the user in the database
    :param username: str | None: Check if the username is a string or none
    :param password: str | None: Update the password of a user
    :param db: Session: Pass the database session to the function
    :return: A user object
    """
    user = db.query(User).filter_by(email=email).first()
>>>>>>> Stashed changes
    user.password = password
    user.username = username
    db.commit()
    return user


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function sets the confirmed field of a user to True.

    :param email: str: Get the email of the user
    :param db: Session: Pass the database session to the function
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Find the user in the database
    :param url: str: Specify the type of parameter that is being passed into the function
    :param db: Session: Pass the database session to the function
    :return: The user object
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def get_users(skip: int, limit: int, db: Session) -> List[User]:
    """
    The get_users function returns a list of users from the database.
    
    :param skip: int: Skip the first n records in the database
    :param limit: int: Limit the number of results returned
    :param db: Session: Pass the database session to the function
    :return: A list of users
    """
    return db.query(User).offset(skip).limit(limit).all()


async def get_user_profile(username: str, db: Session) -> User:
    """
<<<<<<< Updated upstream
    The get_user_profile function returns a UserProfileModel object containing the user's username, email,
    avatar, created_at date and time (in UTC), is_active status (True or False),
    foto count, comment count and rates count.
    
    :param username: str: Get the user profile of a specific user
    :param db: Session: Access the database
    :return: A userprofilemodel object
    """
    user = db.query(User).filter(User.username == username).first()
    if user:
        foto_count = db.query(Image).filter(Image.user_id == user.id).count()
        comment_count = db.query(ImageComment).filter(
            ImageComment.user_id == user.id).count()
=======
    The get_user_profile function returns a UserProfileModel object containing the user's username, email, avatar, created_at date and time (in UTC), is_active status (True or False), photo count and comment count.

    :param username: str: Get the username of the user who is trying to access their profile
    :param db: Session: Pass in the database session to the function
    :return: A user object
    """
    user = db.query(User).filter(User.username == username).first()
    if user:
        photo_count = db.query(Image).filter(Image.user_id == user.id).count()
        comment_count = (
            db.query(ImageComment).filter(ImageComment.user_id == user.id).count()
        )
>>>>>>> Stashed changes
        user_profile = UserProfileModel(
            username=user.username,
            email=user.email,
            avatar=user.avatar,
            created_at=user.created_at,
            is_active=user.is_active,
            photo_count=photo_count,
            comment_count=comment_count,
        )
        return user_profile
    return None


async def make_user_role(email: str, role: Role, db: Session) -> None:

    """
    The make_user_role function takes in an email and a role, and then updates the user's role to that new one.

    :param email: str: Get the user by email
    :param role: UserRoleEnum: Set the role of the user
    :param db: Session: Pass the database session to the function
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.role = role
    db.commit()


'''
                            BAN 
If you haven't been banned, you haven't been in the garden of chat Bizarre :)
'''



async def ban_user(email: str, db: Session) -> None:

    """
    The ban_user function takes in an email and a database session.
    It then finds the user with that email, sets their is_active field to False,
    and commits the change to the database.

    :param email: str: Identify the user to be banned
    :param db: Session: Pass in the database session
    :return: None, because we don't need to return anything
    """
    user = await get_user_by_email(email, db)
    user.is_active = False
    db.commit()


async def remove_from_ban(email: str, db: Session) -> None:
    """
    The remove_from_ban function removes a user from the ban list.

    :param email: str: Get the user by email
    :param db: Session: Pass in the database session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.is_active = True
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


async def activate_user(email: str, db: Session) -> None:
    """
    The activate_user function takes an email and a database session as arguments.
    It then uses the get_user_by_email function to retrieve the user with that email from the database.
    The activate_user function then sets is_active to True for that user, and commits those changes to the database.

    :param email: str: Pass the email of the user to activate
    :param db: Session: Create a database session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.is_active = True
    db.commit()


async def delete_user(user_id: int, db: Session) -> None:
    """
    The delete_user function deletes a user from the database.

    :param user_id: int: Specify the id of the user to be deleted
    :param db: Session: Pass in the database session
    :return: None
    """
    user = db.query(User).filter(User.id == user_id).first()
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

