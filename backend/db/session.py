# db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from.db.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vittasetu_dev.db")

# For SQLite, we need to allow multithreaded access
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
