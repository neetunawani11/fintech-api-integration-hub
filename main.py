
from fastapi import FastAPI, HTTPException, Query

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
