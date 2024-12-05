from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.auth.models import User
from src.database import get_db
from src.auth.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from src.auth.service import create_user, authenticate_user
from src.auth.utils import create_access_token

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    new_user = create_user(db, user)
    access_token = create_access_token({"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    auth_user = authenticate_user(db, user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": auth_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

""" @router.get("/me", response_model=UserResponse)
async def get_current_user_profile(user: UserResponse = Depends(get_current_user)):
    return user
 """