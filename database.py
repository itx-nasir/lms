import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Read database URL from environment (Render provides DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lms.db")

# Some platforms (Heroku, Render) provide a DATABASE_URL that starts with
# "postgres://". SQLAlchemy expects "postgresql://" for the psycopg driver,
# so replace the scheme if necessary.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine. SQLite needs the check_same_thread connect arg.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()