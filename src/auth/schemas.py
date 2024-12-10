from typing import Optional
from datetime import datetime
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, field_serializer, model_validator

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserItem(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(cls, value: datetime) -> Optional[str]:
        if cls is None: 
            return None
        return cls.isoformat()
    class Config:
        from_attributes=True
class UserResponse(BaseModel):
    code: int
    message: str
    result: UserItem
    
class UserLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str
    
    @model_validator(mode='before')
    def check_at_least_one_field(cls, values):
        username = values.get('username')
        email = values.get('email')
        if not username and not email:
            raise RequestValidationError("Either username or email must be provided.")
        return values
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
