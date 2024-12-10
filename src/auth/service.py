from operator import or_
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.auth.models import User
from src.auth.schemas import UserCreate, UserLogin
from src.core.jwt import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user_logic(db: Session, user: UserCreate):
    """
    Business logic for registering a new user.
    """
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )

    # Create a new user
    new_user = create_user(db, user)
    access_token = create_access_token({"sub": new_user.email})

    # Return the access token and other details
    return {"access_token": access_token, "token_type": "bearer"}

def login_user_logic(db: Session, user: UserLogin):
    """
    Business logic for login.
    """
    user_cred = user.email or user.username
    auth_user = authenticate_user(db, user_cred, user.password)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )
    
    access_token = create_access_token({"sub": auth_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )
    db.add(db_user)
    
    # Uncomment to Retrieve Auto-Generated Fields
    # db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, user_cred: str, password: str):
    db_user = db.query(User).filter(
        or_(User.email == user_cred, User.username == user_cred)
    ).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        return None
    return db_user
