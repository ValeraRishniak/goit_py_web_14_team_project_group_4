'''
Main.py налаштований. Можливі зміни лише у підключені routes
'''

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.tags import router as tags_router
from app.routes.photo import router as photo_router
from app.routes.comment import router as comment_router  
from app.database.db import get_db

app = FastAPI()


@app.get("/", name="Project root")
async def root():
    """
    The root function is a simple HTTP endpoint that returns a welcome message.      
    
    :return: A dictionary
    """
    return {"message": "Welcome to Photo SHAKE App"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    """
    The healthchecker function is used to check the health of the database.
    It returns a welcome message if it can connect to the database, and an error message otherwise.

    :param db: Session: Pass the database session to the function
    :return: A dict with a message
    """
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly")
        return {"message": "Database is OK!     \
                Welcome to Photo SHAKE App"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="Error connecting to the database")


app.include_router(auth_router, prefix='/api')
app.include_router(users_router, prefix="/api")
app.include_router(tags_router, prefix="/api")
app.include_router(photo_router, prefix="/api")
app.include_router(comment_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
