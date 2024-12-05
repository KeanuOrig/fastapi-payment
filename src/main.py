from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.database import Base, engine

# Initialize database
Base.metadata.create_all(bind=engine) 

# Initialize the FastAPI application
app = FastAPI( 
    title="Payment Gateway Integration API",
    description="A FastAPI application for integrating a payment gateway",
    version="1.0.0",
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the Payment Gateway Integration API"}