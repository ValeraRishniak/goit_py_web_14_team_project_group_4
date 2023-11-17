from libgravatar import Gravatar
from sqlalchemy.orm import Session
from app.database.models import User
from app.schemas.user import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def get_me(user: User, db: Session):
    """
    The get_me function returns the user object of the currently logged in user.

    :param user: User: Get the user object from the database
    :param db: Session: Access the database
    :return: The user object
    """
    user = db.query(User).filter(User.id == user.id).first()
    return user


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
