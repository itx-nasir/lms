#!/usr/bin/env python3
"""Create or update admin user from environment variables.
Idempotent: will not create a duplicate admin.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import create_tables, SessionLocal
import crud
from dotenv import load_dotenv

load_dotenv()

def seed_admin():
    create_tables()
    db = SessionLocal()
    try:
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')

        existing = crud.get_admin_user(db, admin_username)
        if existing:
            print(f"Admin user '{admin_username}' already exists (id={existing.id}).")
        else:
            crud.create_admin_user(db, admin_username, admin_password)
            print(f"Created admin user: {admin_username}")

    finally:
        db.close()


if __name__ == '__main__':
    seed_admin()
