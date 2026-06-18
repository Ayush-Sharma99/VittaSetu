# db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vittasetu_dev.db")

# Fix Render/Heroku postgres:// -> postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Check if the user accidentally passed an HTTP/HTTPS URL
if DATABASE_URL.startswith("http://") or DATABASE_URL.startswith("https://"):
    import sys
    print("*" * 80, file=sys.stderr)
    print("CRITICAL CONFIGURATION ERROR:", file=sys.stderr)
    print("DATABASE_URL is configured as an HTTP/HTTPS link: " + DATABASE_URL, file=sys.stderr)
    print("A database connection string must start with 'postgresql://' or 'sqlite://'.", file=sys.stderr)
    print("Please check your Render Environment Variables and correct DATABASE_URL.", file=sys.stderr)
    print("Falling back to local SQLite database: sqlite:///./vittasetu_dev.db to prevent crash.", file=sys.stderr)
    print("*" * 80, file=sys.stderr)
    DATABASE_URL = "sqlite:///./vittasetu_dev.db"

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
