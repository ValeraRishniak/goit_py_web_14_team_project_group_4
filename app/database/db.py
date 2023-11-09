from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.conf.config import settings


DATABASE_URL = settings.db_url
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
