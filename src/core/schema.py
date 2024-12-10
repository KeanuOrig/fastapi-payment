from typing import Generic, Optional, TypeVar
from datetime import datetime
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel


T = TypeVar('T')

class ResponseDTO(BaseModel, Generic[T]):
    code: int
    message: str
    result: T
    