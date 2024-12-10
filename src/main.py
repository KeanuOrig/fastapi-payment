from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from src.auth.router import router as auth_router
from src.core.database import Base, engine
from src.auth.models import * 
from src.core.exceptions import http_exception_handler, internal_server_error_handler, validation_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException

# Define the lifespan event handlers
@asynccontextmanager
async def lifespan(application: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")
    yield
    print("Application shutdown complete.")

# Initialize the FastAPI application
app = FastAPI( 
    title="Payment Gateway Integration API",
    description="A FastAPI application for integrating a payment gateway",
    version="1.0.0",
    lifespan=lifespan,
)

# Add custom exceptions
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, internal_server_error_handler)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the Payment Gateway Integration API"}
