import uvicorn
from fastapi import FastAPI

from app.routes import tags

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Photo SHAKE"}


app.include_router(tags.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
