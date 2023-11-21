from typing import List
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader


from app.database.db import get_db
from app.database.models import Role, User
from app.repository import users as repository_users
from app.schemas.user import RequestEmail, RequestRole, UserDb, UserProfileModel
from app.services.auth import auth_service
from app.services.roles import RoleChecker
from app.conf.config import config_cloudinary

router = APIRouter(prefix="/users", tags=["users"])

access_get = RoleChecker([Role.admin, Role.moderator, Role.user])
access_create = RoleChecker([Role.admin, Role.user])
access_update = RoleChecker([Role.admin, Role.moderator, Role.user])
access_delete = RoleChecker([Role.admin, Role.user])
access_admin = RoleChecker([Role.admin])


@router.get("/me/", response_model=UserDb, dependencies=[Depends(access_get)])
async def read_users_me(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    user = await repository_users.get_me(current_user, db)
    return user


@router.patch('/update_user_access_info', response_model=UserDb, dependencies=[Depends(access_create)])
async def update_all_inform_user(
        username: str | None,
        password: str | None,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)):
    user = await repository_users.update_user_inform(current_user.email,
                                                     username,
                                                     password,
                                                     db)
    return user


@router.patch('/update avatar', response_model=UserDb, dependencies=[Depends(access_create)])
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    config_cloudinary()

    r = cloudinary.uploader.upload(
        file.file, public_id=f'PhotoSHAKE/{current_user.id}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'PhotoSHAKE/{current_user.id}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user


@router.get("/all", response_model=List[UserDb],
            dependencies=[Depends(access_get)]
            )
async def read_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    The read_all_users function returns a list of users.
        ---
        get:
          summary: Returns all users.
          description: This can only be done by the logged in user.
          operationId: read_all_users
          parameters:
            - name: skip (optional)  # The number of records to skip before returning results, default is 0 (no records skipped).  Used for pagination purposes.   See https://docs.mongodb.com/manual/reference/method/cursor.skip/#cursor-skip-examples for more information on how this

    :param skip: int: Skip the first n records
    :param limit: int: Limit the number of results returned
    :param db: Session: Pass the database connection to the function
    :return: A list of users
    """
    users = await repository_users.get_users(skip, limit, db)
    return users


@router.get("/user_profile_with_username/{username}", response_model=UserProfileModel,
            dependencies=[Depends(access_get)]
            )
async def read_user_profile_by_username(username: str, db: Session = Depends(get_db),
                                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_user_profile_by_username function is used to read a user profile by username.
        The function takes in the username as an argument and returns the user profile if it exists.

    :param username: str: Get the username from the url path
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user's information
    :return: A userprofile object
    """
    user_profile = await repository_users.get_user_profile(username, db)
    if user_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='NOT FOUND')
    return user_profile


@router.patch("/make_role/{email}/",
              dependencies=[Depends(access_admin)]
              )
async def make_role_by_email(body: RequestRole, db: Session = Depends(get_db)):
    """
    The make_role_by_email function is used to change the role of a user.
        The function takes in an email and a role, and changes the user's role to that specified by the inputted
        parameters. If no such user exists, then an HTTPException is raised with status code 401 (Unauthorized)
        and detail message &quot;Invalid Email&quot;. If the new role matches that of the current one, then a message saying so
        will be returned. Otherwise, if all goes well, then a success message will be returned.

    :param body: RequestRole: Get the email and role from the request body
    :param db: Session: Access the database
    :return: A dictionary with a message key
    """
    user = await repository_users.get_user_by_email(body.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    if body.role == user.role:
        return {"message": "Role is already exists"}
    else:
        await repository_users.make_user_role(body.email, body.role, db)
        return {"message": f"User role changed to {body.role.value}"}


@router.patch("/ban/{email}/",
              dependencies=[Depends(access_admin)]
              )
async def ban_user_by_email(body: RequestEmail, db: Session = Depends(get_db)):
    """
    The ban_user_by_email function takes a user's email address and bans the user from accessing the API.
        If the email is not found in our database, an HTTPException is raised with status code 401 (Unauthorized) and
        detail message &quot;Invalid Email&quot;. If the user has already been banned, an HTTPException is raised with status code 409
        (Conflict) and detail message &quot;User Already Not Active&quot;. Otherwise, if no exceptions are thrown, we return a JSON object
        containing key-value pair {&quot;message&quot;: USER_NOT_ACTIVE}.

    :param body: RequestEmail: Get the email from the request body
    :param db: Session: Get the database session
    :return: A dictionary with a message
    """
    user = await repository_users.get_user_by_email(body.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    if user.is_active:
        await repository_users.ban_user(user.email, db)
        return {"message": "User is banned"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already is banned")


@router.patch("/remove from ban/{email}/", response_model=UserDb,
              dependencies=[Depends(access_admin)])
async def remove_from_ban(body: RequestEmail, db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    if not user.is_active:
        await repository_users.activate_user(user.email, db)

        return {"message": "User removed from ban"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='This email is already active')


@router.delete("/delete user/{user_id}", response_model=UserDb,
               dependencies=[Depends(access_admin)])
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    us = await repository_users.delete_user(user_id, db)
    if us is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return us
