from libgravatar import Gravatar
from sqlalchemy.orm import Session
from app.database.models import User, Role, Image, ImageComment
from app.schemas.user import UserModel, UserResponse, UserDb
from sqlalchemy import select, func
from sqlalchemy.orm.exc import NoResultFound

async def get_user_by_email(email: str, db: Session) -> User | None:
    user = db.query(User).filter_by(email=email).first()
    return user

async def get_me(user: User, db: Session):
    user = db.query(User).filter(User.id == user.id).first()
    return user

async def create_admin_user(user: User, db: Session) :
    admin = db.query(User).filter(User.id == user.id).first()
    admin.role = Role.admin
    db.commit()
    return admin

async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    
    user = User( avatar= avatar, **body.dict())
    user.role = Role.user
    result =   db.execute(select(User))
    userscount = len(result.all())
    if not userscount:
        user.role= Role.admin
    
    db.add(user)

    db.commit()

    db.refresh(user)

    return user    

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

async def update_user_inform(email:str, 
                             username:str|None, 
                            password:str|None,
                             db: Session) -> User:
    user =  db.query(User).filter_by(email=email).first()
    user.password = password
    user.username = username
    db.commit()
    return user

async def make_user_role(email: str, role: Role, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.role = role
    try:
       db.commit()
    except Exception as e:
        db.rollback()
        raise e


async def get_user_by_username(username: str, db: Session) -> User | None:
    try:
             return  db.scalar(select(User).filter(User.username == username)) 
    except NoResultFound:
        return None

  
async def ban_user(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.is_active = False
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e

async def razban_user(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.is_active = True
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    
async def get_users(skip: int, limit: int, db: Session) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()

async def delete_user(user_id : int, db: Session) -> None:
      user = db.query(User).filter(User.id == user_id).first()
      db.delete(user)
      db.commit()
      return user
