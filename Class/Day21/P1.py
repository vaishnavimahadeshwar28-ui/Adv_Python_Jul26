# Request body validation
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, validator, Field, EmailStr
from typing import List
app = FastAPI()

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(...,min_length=8)

    @validator('password')
    def validate_password(cls,v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
                    raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
                    raise ValueError('Password must contain at least one number')
        return v

class UserRegistration(BaseModel):
       username: str
       email: EmailStr
       password: str
       password_confirm: str

       @validator('password_confirm')
       def passwords_match(cls, v, values):
            if 'password' in values and v!=values['password']:
                   raise ValueError('Passwords do not match')
            return v

@app.post("/login")
async def login(login_data:UserLogin):
       if login_data.username == "admin" and login_data.password == "Admin123!":
              return {"message": "Login succesful", "token":"fake-jwt-token" }

       raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid credentials"
       )
              
@app.post("/register")
async def register(user_data:UserRegistration):
       return{
              "message": "User registered successfully",
              "user":{
                     "username": user_data.username,
                     "email":user_data.email
              }
       }       
                   
# Run our application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "P1:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )