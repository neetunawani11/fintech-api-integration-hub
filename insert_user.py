
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import engine
from models import User


with Session(engine) as session:

    # Check whether our demo user already exists
    existing_user = session.scalar(
        select(User).where(
            User.email == "demo101@example.com"
        )
    )

    if existing_user:
        print("Demo user already exists.")
    else:
        # Create a fictional user
        new_user = User(
            name="Demo User A",
            email="demo101@example.com"
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        print("User created successfully!")
        print("User ID:", new_user.id)
        print("Name:", new_user.name)
        print("Email:", new_user.email)
