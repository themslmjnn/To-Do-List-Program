from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from db.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()