from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.jwt import decode_jwt_token
from src.auth.models import User
from src.core.database import get_db
from fastapi.security import OAuth2PasswordBearer

# OAuth2PasswordBearer is used to extract the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = decode_jwt_token(token)
    
    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user