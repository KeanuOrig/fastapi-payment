from datetime import datetime, timezone, timedelta
import os
import jwt
from typing import Union
from fastapi import HTTPException, status
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.auth.models import User
from src.auth.schemas import UserItem
from src.core.database import get_db
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Expire in 30 minutes
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables!")

# OAuth2PasswordBearer is used to extract the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Generate a JWT token with a specified expiration time.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # Get the email from the token payload
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid")
        return email
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid or expired")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Extract user from the database using the token.
    """
    # Decode the token to get the user email
    email = decode_jwt_token(token)
    
    # Retrieve user from the database by email
    user = db.query(User).filter(User.email == email).first()
    
    # If the user is not found, raise a 404 HTTP exception
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    # Return the user object if found
    return UserItem.model_validate(user)