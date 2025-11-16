#!/usr/bin/env python
"""Seed Testuser account into the database."""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from models import SessionLocal, User, Base, engine
from auth import hash_password

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    # Check if Testuser exists
    existing = db.query(User).filter(User.username == "Testuser").first()
    if existing:
        print(f"✓ Testuser already exists: id={existing.id}, email={existing.email}")
    else:
        print("Creating Testuser...")
        test_user = User(
            username="Testuser",
            email="testuser@example.com",
            hashed_password=hash_password("1234"),
            full_name="Test User",
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✓ Created Testuser: id={test_user.id}, username={test_user.username}")

    # List all users
    all_users = db.query(User).all()
    print(f"\nTotal users: {len(all_users)}")
    for u in all_users:
        print(f"  - {u.username} ({u.email})")
finally:
    db.close()
