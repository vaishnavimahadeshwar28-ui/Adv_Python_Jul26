# Request body & Pydantic Models
# Pydantic Models: are py classes that define the structure of data, providing automatic 
# validation, serailization and documentation(Swagger)

from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime

app = FastAPI()
class UserCreate(BaseModel):
    name: str = Field(...,min_length=2,max_length=50,description="User's full name")
    email: EmailStr = Field(...,description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=100, description="User's age")
    is_active: bool = Field(True, description="Whether the user is active")
    tags: List[str] = Field(default=[], description="User tags")

@app.post("/users")
async def create_user(user:UserCreate):
    return{
        "message":"User created successfully",
        "user":user,
        "user_id":123
    }

# Run our application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "P3:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
# Use the following URL to test
# http://127.0.0.1:8000/docs
# Request body:
"""
{
  "name": "Vaishnavi",
  "email": "vaishnavi@2gmail.com",
  "age": 19,
  "is_active": true,
  "tags": [
    "developer",
    "Trainer"]
}
"""