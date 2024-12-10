from datetime import datetime
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from contextlib import contextmanager
from typing import Callable, Any, Optional
from sqlalchemy.exc import SQLAlchemyError

# Utility function for API responses
def api_response(code: int = 200, message: str = 'Good', result: Any = [], error: Optional[str] = None):
    if error:
        content = {
            "code": code,
            "message": message,
            "error": error
        }
    else:
        content = {
            "code": code,
            "message": message,
            "result": result
        }
        
    return JSONResponse(
        status_code=code,
        content=content
    )

# Context manager for handling database sessions
@contextmanager
def transaction(db: Session):
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

# Function to execute a callable within a transaction
def run_in_transaction(callable_function: Callable, db: Session, *args, **kwargs):
    try:
        with transaction(db):
            data = callable_function(db, *args, **kwargs)
            return api_response(200, "Good", result=data)
    except RequestValidationError as e:
        return api_response(422, "Validation Error", result=[])
    except HTTPException as e:
        return api_response(e.status_code, "Client Error", result=[], error=e.detail)
    except SQLAlchemyError as e:
        return api_response(500, "Database Error", result=[], error=str(e.orig) if hasattr(e, 'orig') else str(e))
    except Exception as e:
        return api_response(500, "Internal Server Error", result=[], error=str(e))
