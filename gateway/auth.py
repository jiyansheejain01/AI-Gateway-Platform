"""
Authentication and authorization mechanisms.
Handles API key validation, JWT parsing, and role-based access control (RBAC).
"""
from jose import jwt

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
 