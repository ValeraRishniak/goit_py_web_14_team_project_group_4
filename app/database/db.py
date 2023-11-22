from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.conf.config import settings


DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    The get_db function opens a new database connection if there is none yet for the current application context.
    It will also create the database tables if they don't exist yet.

    :return: A context manager that provides a database session
    """
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
