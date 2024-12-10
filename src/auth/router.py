from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.auth.schemas import UserCreate, UserItem, UserLogin, UserResponse, TokenResponse
from src.core.jwt import get_current_user
from src.core.schema import ResponseDTO
from src.core.utils import api_response, run_in_transaction
from src.auth.service import register_user_logic, login_user_logic

router = APIRouter()

@router.post("/register", response_model=ResponseDTO[TokenResponse])
def register_user(
        user: UserCreate, 
        db: Session = Depends(get_db)
    ):
    return run_in_transaction(register_user_logic, db, user)

@router.post("/login", response_model=ResponseDTO[TokenResponse])
def login_user(
        user: UserLogin, 
        db: Session = Depends(get_db)
    ):
    return run_in_transaction(login_user_logic, db, user)

@router.get("/me", response_model=ResponseDTO[UserItem])
def get_current_user_profile(
        user: UserItem = Depends(get_current_user)
    ):
    return api_response(result=user.model_dump())