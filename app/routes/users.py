from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from redis.asyncio import Redis

from app.database.db import get_db
from app.database.models import User, Role
from app.repository import users as repository_users
from app.services.auth import auth_service
from app.conf.config import settings, init_async_redis
from app.schemas.user import UserDb, UserResponse
from app.services.roles import Admin_Moder, Admin
from app.conf.config import config_cloudinary
from app.services.emailtogo import send_email

router = APIRouter(prefix="/users", tags=["users"])


# @router.patch("/admin/create", response_model=UserDb )
# async def create_admin(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
#     admin = await repository_users.create_admin_user(current_user , db)
#     return admin
    

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


@router.patch('/update_all_inform_user', response_model=UserDb)
async def update_all_inform_user( 
                                 username: str| None,
                                password: str|None, 
                                 current_user: User = Depends(auth_service.get_current_user),
                                 db: Session = Depends(get_db)):       
    user = await repository_users.update_user_inform(current_user.email, 
                                                     username, 
                                                    password,  
                                                     db)
    return user

@router.get("/all Users/", response_model=list[UserDb])
async def read_all_users(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    return await repository_users.get_users(skip, limit, db)

@router.patch("/asign_role/{role}",  dependencies=[Depends(Admin_Moder)] , response_model=UserDb)
async def assign_role( email: str, role: Role, db: Session = Depends(get_db)): 
    user = await repository_users.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.role == role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user already has this role installed")

    return await repository_users.make_user_role(email, role, db)
   

@router.get("/{username}", response_model=UserDb)
async def get_user_by_username( username: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)) -> dict | None:
  
    user = await repository_users.get_user_by_username(username, db)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="This not found")

@router.get("/find_by_mail/{by_email}", response_model=UserDb)
async def get_user_by_email( email: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)) -> dict | None:
     user  = await repository_users.get_user_by_email(email, db)
     return user 
 
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

@router.patch("/razban", name="razban_user", dependencies=[Depends(Admin)], response_model=UserDb)
async def razban_user( email: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(email, db)

    if user.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'You razban yourself')

    if not user:
        raise HTTPException(status_code=404, detail="No this Email")

    if not user.is_active:
        await repository_users.activate_user(user.email, db)

        return {"message": "User is razbanned"}
    else:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='This email is already active')

@router.delete("/{user_id}", dependencies=[Depends(Admin_Moder)], response_model=UserDb)
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    us = await repository_users.delete_user(user_id, db)
    if us is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return us