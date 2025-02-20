
from sqlalchemy import create_engine
import os

from sqlalchemy.orm import sessionmaker, declarative_base

# # sqlite
# DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# postgres
DATABASE_URL =os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_14DdOnUeWIEy@ep-royal-truth-a8og4dj3-pooler.eastus2.azure.neon.tech/neondb?sslmode=require")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


