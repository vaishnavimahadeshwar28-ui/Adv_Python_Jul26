# Dependency injection: 
# Needs to be discussed

from fastapi import FastAPI, Depends, Header, HTTPException


from typing import Optional


app = FastAPI()


# ===== Simple Dependency =====


def get_db():


    """


    Dependency that returns a database connection.


    """


    # In real app, this would create/return a connection


    print("Creating database connection")


    return {"connection": "db_connection", "status": "connected"}


@app.get("/users")


async def get_users(db: dict = Depends(get_db)):


    """


    Endpoint that uses the database dependency.


    """


    return {


        "message": "Getting users",


        "db_status": db["status"],


        "users": ["Alice", "Bob", "Charlie"]


    }


# ===== Dependency with Parameters =====


def get_pagination(skip: int = 0, limit: int = 10):


    """


    Dependency for pagination.


    """


    return {"skip": skip, "limit": limit}


@app.get("/items")


async def get_items(pagination: dict = Depends(get_pagination)):


    """


    Endpoint with pagination dependency.


    """


    return {


        "pagination": pagination,


        "items": [f"Item {i}" for i in range(pagination['skip'], pagination['skip'] + pagination['limit'])]


    }


# ===== Dependency for Authentication =====


async def get_current_user(token: str = Header(...)):


    """


    Dependency that validates the user token.


    """


    if token != "secret-token":


        raise HTTPException(status_code=401, detail="Invalid token")


   


    return {"id": 1, "username": "alice", "role": "admin"}


@app.get("/profile")


async def get_profile(user: dict = Depends(get_current_user)):


    """


    Endpoint that requires authentication.


    """


    return {"user": user}


# ===== Nested Dependencies =====


async def get_optional_user(token: Optional[str] = Header(None)):


    """Dependency that gets user if token exists."""


    if token and token == "secret-token":


        return {"id": 1, "username": "alice"}


    return None


async def get_optional_db(connection: str = "default"):


    """Dependency that gets database connection."""


    return {"connection": connection}


@app.get("/public")


async def public_endpoint(


    db: dict = Depends(get_optional_db),


    user: Optional[dict] = Depends(get_optional_user)


):


    """


    Endpoint that works with or without authentication.


    """


    return {


        "message": "Public endpoint",


        "user": user,


        "db": db


    }


# ============================================================
# RUN APPLICATION
# ============================================================


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "P2:app",  # Replace test with your filename without .py
        host="127.0.0.1",
        port=8000,
        reload=True
    )
