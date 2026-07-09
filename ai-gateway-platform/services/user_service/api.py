"""
API endpoints for user and client management.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import FastAPI, HTTPException, Header
from gateway.rate_limiter import check_rate_limit
from pydantic import BaseModel

from services.user_service.database import SessionLocal, engine
from services.user_service.models import Base, User

from core.config import settings
from jose import jwt, JWTError

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        return None

app = FastAPI()

Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class LoginRequest(BaseModel):
    username: str
    password: str

def create_access_token(data: dict):
    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

@app.post("/users")
def create_user(user: UserCreate):

    db = SessionLocal()

    new_user = User(
        username=user.username,
        password=user.password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "role": new_user.role
    }

@app.post("/login")
def login(user: LoginRequest):

    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if db_user.password != user.password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    token = create_access_token(
        {
            "username": db_user.username,
            "role": db_user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/users")
def get_users():

    allowed = check_rate_limit("global_user")

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )

    db = SessionLocal()

    users = db.query(User).all()

    return users

'''
@app.get("/admin/users")
def admin_get_users(
    #authorization: str = Header(default=None)
    token: str
):

    print("AUTH HEADER =", authorization)

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    if payload["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    db = SessionLocal()

    users = db.query(User).all()

    return users 
    '''

@app.get("/admin/users")
def admin_get_users(token: str):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    if payload["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    db = SessionLocal()

    return db.query(User).all()