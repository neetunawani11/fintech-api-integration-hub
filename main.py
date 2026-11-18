
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import engine
from models import User


app = FastAPI(
    title="Fintech API Integration Hub",
    description="A Python backend learning project",
    version="0.1.0"
) 


# --------------------------------
# HOME API
# --------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Fintech API Integration Hub",
        "status": "running"
    }


# --------------------------------
# ABOUT API
# --------------------------------

@app.get("/about")
def about():
    return {
        "project": "Fintech API Integration Hub",
        "developer": "Neetu Nawani",
        "purpose": "Learning Python API Development",
        "version": "1.0"
    }


# --------------------------------
# FICTIONAL USER DATA
# --------------------------------

users = {
    101: {
        "name": "Demo User A",
        "email": "user101@example.com",
        "balance": 5000
    },
    102: {
        "name": "Demo User B",
        "email": "user102@example.com",
        "balance": 12000
    },
    103: {
        "name": "Demo User C",
        "email": "user103@example.com",
        "balance": 7500
    }
}


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr

# --------------------------------
# GET ALL USERS
# Query parameter example
# --------------------------------

@app.get("/users")
def list_users(
    limit: int = Query(default=10, ge=1, le=100)
):
    user_list = [
        {"user_id": user_id, **user_data}
        for user_id, user_data in users.items()
    ]

    return {
        "total": len(user_list),
        "users": user_list[:limit]
    }


# --------------------------------
# GET USER BY ID
# Path parameter example
# --------------------------------

@app.get("/users/{user_id}")
def get_user(user_id: int):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": user_id,
        "user": users[user_id]
    }


# --------------------------------
# FICTIONAL ACCOUNT DATA
# --------------------------------

accounts = {
    201: {
        "owner": "Demo User A",
        "balance": 5000
    },
    202: {
        "owner": "Demo User B",
        "balance": 12000
    },
    203: {
        "owner": "Demo User C",
        "balance": 7500
    }
}


# --------------------------------
# GET ACCOUNT BALANCE
# --------------------------------

@app.get("/accounts/{account_id}/balance")
def get_balance(account_id: int):

    if account_id not in accounts:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    account = accounts[account_id]

    return {
        "account_id": account_id,
        "owner": account["owner"],
        "balance": account["balance"],
        "currency": "INR"
    }

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):

    # Check for duplicate email addresses
    for existing_user in users.values():
        if existing_user["email"].lower() == str(user.email).lower():
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

    # Generate a new fictional user ID
    new_user_id = max(users.keys(), default=100) + 1

    # Store the new user in memory
    users[new_user_id] = {
        "name": user.name,
        "email": str(user.email),
        "balance": 0
    }

    # Return the newly created user
    return {
        "message": "User created successfully",
        "user_id": new_user_id,
        "user": users[new_user_id]
    }

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate):

    # Check if the fictional user exists
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Prevent using another user's email
    for existing_id, existing_user in users.items():
        if existing_id != user_id:
            if existing_user["email"].lower() == str(user.email).lower():
                raise HTTPException(
                    status_code=409,
                    detail="Email already registered"
                )

    # Update allowed profile fields
    users[user_id]["name"] = user.name
    users[user_id]["email"] = str(user.email)

    return {
        "message": "User updated successfully",
        "user_id": user_id,
        "user": users[user_id]
    }

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check for duplicate email
    for existing_id, existing_user in users.items():
        if existing_id != user_id:
            if existing_user["email"].lower() == str(user.email).lower():
                raise HTTPException(
                    status_code=409,
                    detail="Email already registered"
                )

    # Update the user's profile
    users[user_id]["name"] = user.name
    users[user_id]["email"] = str(user.email)

    return {
        "message": "User updated successfully",
        "user_id": user_id,
        "user": users[user_id]
    }

class UserPatch(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    email: EmailStr | None = None

@app.patch("/users/{user_id}")
def patch_user(user_id: int, changes: UserPatch):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    update_data = changes.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update"
        )

    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=422,
            detail="Name and email cannot be null"
        )

    if "email" in update_data:
        new_email = str(update_data["email"])

        for existing_id, existing_user in users.items():
            if existing_id != user_id:
                if existing_user["email"].lower() == new_email.lower():
                    raise HTTPException(
                        status_code=409,
                        detail="Email already registered"
                    )

        update_data["email"] = new_email

    users[user_id].update(update_data)

    return {
        "message": "User partially updated successfully",
        "user_id": user_id,
        "user": users[user_id]
    }

# --------------------------------
# GET USERS FROM POSTGRESQL
# --------------------------------

@app.get("/db/users")
def get_database_users():

    with Session(engine) as session:

        statement = select(User).order_by(User.id)

        db_users = session.scalars(statement).all()

        return {
            "total": len(db_users),
            "users": [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
                for user in db_users
            ]
        }

# --------------------------------
# CREATE USER IN POSTGRESQL
# --------------------------------

@app.post("/db/users", status_code=201)
def create_database_user(user: UserCreate):

    with Session(engine) as session:

        new_user = User(
            name=user.name,
            email=str(user.email)
        )

        session.add(new_user)

        try:
            session.commit()
            session.refresh(new_user)

        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

        return {
            "message": "User saved to database",
            "user_id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }

# --------------------------------
# UPDATE USER IN POSTGRESQL
# --------------------------------

@app.put("/db/users/{user_id}")
def update_database_user(user_id: int, user: UserCreate):

    with Session(engine) as session:

        # Find the user in PostgreSQL
        db_user = session.get(User, user_id)

        if db_user is None:
            raise HTTPException(
                status_code=404,
                detail="Database user not found"
            )

        # Check whether another user owns the email
        existing_email = session.scalar(
            select(User).where(
                User.email == str(user.email),
                User.id != user_id
            )
        )

        if existing_email is not None:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

        # Update the user details
        db_user.name = user.name
        db_user.email = str(user.email)

        try:
            session.commit()
            session.refresh(db_user)
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Database constraint conflict"
            )

        return {
            "message": "Database user updated successfully",
            "user_id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }

@app.patch("/db/users/{user_id}")
def patch_database_user(user_id: int, changes: UserPatch):

    with Session(engine) as session:

        db_user = session.get(User, user_id)

        if db_user is None:
            raise HTTPException(
                status_code=404,
                detail="Database user not found"
            )

        update_data = changes.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="Provide at least one field to update"
            )

        if any(value is None for value in update_data.values()):
            raise HTTPException(
                status_code=422,
                detail="Name and email cannot be null"
            )

        if "email" in update_data:
            new_email = str(update_data["email"])

            existing_email = session.scalar(
                select(User).where(
                    User.email == new_email,
                    User.id != user_id
                )
            )

            if existing_email is not None:
                raise HTTPException(
                    status_code=409,
                    detail="Email already registered"
                )

            update_data["email"] = new_email

        for field, value in update_data.items():
            setattr(db_user, field, value)

        try:
            session.commit()
            session.refresh(db_user)
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Database constraint conflict"
            )

        return {
            "message": "Database user partially updated",
            "user_id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }

# --------------------------------
# DELETE USER FROM POSTGRESQL
# --------------------------------

@app.delete("/db/users/{user_id}")
def delete_database_user(user_id: int):

    with Session(engine) as session:

        # Find the fictional user
        db_user = session.get(User, user_id)

        if db_user is None:
            raise HTTPException(
                status_code=404,
                detail="Database user not found"
            )

        # Save details before deletion
        deleted_user = {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }

        # Delete the user
        session.delete(db_user)
        session.commit()

        return {
            "message": "Database user deleted successfully",
            "deleted_user": deleted_user
        }
