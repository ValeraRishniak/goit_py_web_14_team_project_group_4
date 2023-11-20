from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from redis.asyncio import Redis

from app.database.db import get_db
from app.database.models import User, Role
from app.repository import users as repository_users
from app.services.auth import auth_service
from app.conf.config import settings, init_async_redis
from app.schemas.user import UserDb
from app.services.roles import Admin_Moder, Admin
from app.conf.config import config_cloudinary

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_my_users(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    user = await repository_users.get_me(current_user, db)
    return user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    config_cloudinary()

    r = cloudinary.uploader.upload(
        file.file, public_id=f'PhotoSHAKE/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'PhotoSHAKE/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user

@router.patch("/asign_role/{role}", dependencies=[Depends(Admin)], response_model=UserDb)
async def assign_role( email: str, role: Role, db: Session = Depends(get_db), redis_client: Redis = Depends(init_async_redis)):
    
    key_to_clear = f"user:{email}"
    await redis_client.delete(key_to_clear)

    user = await repository_users.get_user_by_email(email, db)

    if not user:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="No this Email")

    if role == user.role:
        return {"message": "Role is already exists"}
    else:
        await repository_users.make_user_role(email, role, db)
        return {"message": f"User role changed to {role.value}"}



@router.get("/{username}", response_model=UserDb)
async def user_profile( username: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)) -> dict | None:
  
    user = await repository_users.get_user_by_username(username, db)

    if user:
        urer_profile = await repository_users.get_user_by_username(current_user.username, db)
        return urer_profile
    else:
        raise HTTPException(status_code=404, detail="This not found")

@router.patch("/ban", name="ban_user", dependencies=[Depends(Admin)],  response_model=UserDb)
async def ban_user( email: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
  
    user = await repository_users.get_user_by_email(email, db)

    if not user:
        raise HTTPException(status_code=404, detail="No this Email")

    if user.id == current_user.id:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="It`s yourself")

    if user.is_active:
        await repository_users.ban_user(user.email, db)

        return {"message": "User is banned"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You banned this User")
