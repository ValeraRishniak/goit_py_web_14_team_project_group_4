from libgravatar import Gravatar
from sqlalchemy.orm import Session
from app.database.models import User, Role, Image, ImageComment
from app.schemas.user import UserModel, UserResponse
from sqlalchemy import select, func
from sqlalchemy.orm.exc import NoResultFound

async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def get_me(user: User, db: Session):
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
    new_user.role = Role.user
    # якщо юзеров небулу створює админ
    users_result = await db.execute(select(User))
    users_count = len(users_result.scalars().all())
    if not users_count:
        new_user.role = Role.admin
            
        try:
                db.add(new_user)
                await db.commit()
                await db.refresh(new_user)
                return new_user
        except Exception as e:
                await db.rollback()
                raise e


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


async def make_user_role(email: str, role: Role, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.role = role
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def get_user_by_username(username: str, db: Session) -> User | None:
    try:
        result = await db.execute(select(User).filter(User.username == username))
        return result
    except NoResultFound:
        return None
    
async def get_user_profile(username: str, db: Session) -> User:
    query = select(User).filter(User.username == username)
    user = await db.execute(query)

    if user:
        user_profile = UserResponse(
            id=user.id,
            role=user.role,
            username=user.username,
            email=user.email,
            avatar=user.avatar,
            create_at=user.created_at,
            is_active=user.is_active,
        )
        return user_profile
    return None
  
async def ban_user(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.is_active = False
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e

