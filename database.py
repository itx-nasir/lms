import os
import sys
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Read database URL from environment (Render provides DATABASE_URL)
DB_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "LMS")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "lms.db")


def _bundled_db_candidates():
    """Locations where the installer/PyInstaller may have shipped lms.db."""
    candidates = []
    if getattr(sys, "frozen", False):
        # PyInstaller onedir: datas land in sys._MEIPASS (…\_internal)
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidates.append(os.path.join(meipass, "lms.db"))
        # Also check next to the .exe, in case it was placed there manually
        candidates.append(os.path.join(os.path.dirname(sys.executable), "lms.db"))
    else:
        # Dev / non-frozen: project folder next to this file
        candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lms.db"))
    return candidates


def ensure_local_db():
    """
    On first run, copy the bundled seed DB into %APPDATA%\\LMS\\lms.db.
    Never overwrite an existing user database.
    """
    if os.path.exists(DB_PATH):
        return
    for src in _bundled_db_candidates():
        if src and os.path.isfile(src) and os.path.abspath(src) != os.path.abspath(DB_PATH):
            shutil.copy2(src, DB_PATH)
            return


ensure_local_db()
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

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