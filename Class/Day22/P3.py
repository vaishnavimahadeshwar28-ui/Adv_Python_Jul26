# JWT Authentication
# pip install python-jose[cryptography] passlib[bcrypt]
# pip install bcrypt

from datetime import  datetime, timedelta, timezone
from typing import Optional
import bcrypt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

app = FastAPI()

# Configuration
SECRET_KEY = "Your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing: bcrypt
def verify_password(plain_password:str,hashed_password: str)->bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def get_password_hash(password:str)->str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

# JWT Function
def create_access_token(data:dict, expires_delta:Optional[timedelta]=None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# Oauth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Fake DB
fake_users_db = {
    "rakesh": {
        "username": "rakesh",
        "email": "r@r.com",
        "full_name": "Rakesh Aradhya",
        "hashed_password": get_password_hash("secret123"),
        "disabled": False,
    },
    "bipin": {
            "username": "bipin",
            "email": "bip@r.com",
            "full_name": "Bipin Aradhya",
            "hashed_password": get_password_hash("secret456"),
            "disabled": True,
        },
}

def get_user(db,username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

# Authentication Function
async def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db,username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False

    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current user from the JWT token."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User=Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

# Authorization function
async def get_current_admin_user(current_user: User=Depends(get_current_active_user)):
    if current_user.username != "rakesh":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

# Authentication Endpoints
@app.post("/token",response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers = {"WWW-Authenticate":"Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub":user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type":"bearer"}


# Protected endpoints
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """Get current user's items."""
    return [
        {"item_name": "My Item 1", "owner": current_user.username},
        {"item_name": "My Item 2", "owner": current_user.username}
    ]

@app.get("/admin")
async def admin_endpoint(current_user: User = Depends(get_current_admin_user)):
    """Admin-only endpoint."""
    return {"message": f"Welcome admin {current_user.username}"}


# ============================================================
# RUN APPLICATION
# ============================================================
if __name__ == "__main__":
    import uvicorn


    uvicorn.run(
        "P3:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )