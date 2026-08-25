# Response Models
# Reponse models define the structure and type of data returned by API endpoints.
# Provides automatic validation, serialization and documentation of responses.

from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()

# Response Models
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool

    # Pydantic configuration
    model_config = ConfigDict(from_attributes=True)

class UserListResponse(BaseModel):
    total: int
    users: List[UserResponse]

class ErrorResponse(BaseModel):
    error: str
    detail: str
    timestamp: datetime

@app.get("/")
async def root():
    return {
        "message":"Welcome to the User Api",
        "available_endpoints":[
            "GET /users",
            "GET /users/{user_id}",
            "GET /docs"
        ]
    }

@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={
        404: {
            "model":ErrorResponse,
            "description": "User not found"
        }
    }
)
async def get_user(user_id:int):
    if user_id == 1:
        return{
            "id":1,
            "username":"rakesh",
            "email": "r@r.com",
            "created_at": datetime.now(),
            "is_active": True
        }

    raise HTTPException(
        status_code=404,
        detail={
            "error": "Not found",
            "detail" : f"User {user_id} not found",
            "timestamp": datetime.now().isoformat()
        }
    )

@app.get("/users",response_model=UserListResponse)
async def get_users(
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of users to skip"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of users to return"
    )
):
    users = [
        {
            "id":i,
            "username":f"user_{i}",
            "email":f"user_{i}@example.com",
            "created_at":datetime.now(),
            "is_active":True
        }
        for i in range (1,6)
    ]
    paginated_users = users[skip:skip+limit]
    return {
        "total": len(users),
        "users": paginated_users
    }

# Run our application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "P2:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )