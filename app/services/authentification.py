from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.database.db import get_db
from app.database.models  import User
from app.database import SessionLocal
from app.schemas.photo_tags import PhotoModels

SECRET_KEY = "Photo_SHAKE_123"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None
    roles: List[str] = []

#3 ролі користувачів і іхні різні права доступу
def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception, db)

def get_user_by_username(username: str, db: SessionLocal):
    return db.query(User).filter(User.username == username).first()

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user is None or "inactive" in current_user.roles:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_moderator_user(current_user: User = Depends(get_current_user)):
    if "moderator" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user

# Функція для генерації JWT токена
def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Функція для верифікації JWT токена
def verify_token(token: str, credentials_exception, db: SessionLocal):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, roles=payload.get("roles"))
    except JWTError:
        raise credentials_exception
    return token_data

async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends(), db: SessionLocal = Depends(get_db)):
    username = form_data.username
    password = form_data.password

    user = get_user_by_username(username, db)

    if user and password == user.password:
        token_data = {"sub": username, "roles": user.roles}
        access_token = create_token(token_data)
        return Token(access_token=access_token, token_type="bearer")

    # Якщо ім'я користувача або пароль невірні, викидаємо HTTPException зі статусом 401
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
#Функція посту для різних рівнів користувачів
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends()):
    # Реалізуйте вашу логіку для отримання та перевірки користувача та генерації токена
    pass

@app.post("/private-route", response_model=str)
async def private_route(
    photo: PhotoModels,
    current_user: User = Depends(get_current_active_user),
    db: SessionLocal = Depends(SessionLocal),
):
    added_photo = await add_photo(photo, current_user, db)
    return f"Photo uploaded by {current_user.username}. Photo ID: {added_photo.id}"

@app.post("/moderator-route", response_model=str)
async def moderator_route(
    photo: PhotoModels,
    current_user: User = Depends(get_current_moderator_user),
    db: SessionLocal = Depends(SessionLocal),
):
    added_photo = await add_photo(photo, current_user, db)
    return f"Photo processed by moderator {current_user.username}. Photo ID: {added_photo.id}"

@app.post("/admin-route", response_model=str)
async def admin_route(
    photo: PhotoModels,
    current_user: User = Depends(get_current_admin_user),
    db: SessionLocal = Depends(SessionLocal),
):
    added_photo = await add_photo(photo, current_user, db)
    return f"Photo processed by admin {current_user.username}. Photo ID: {added_photo.id}"
