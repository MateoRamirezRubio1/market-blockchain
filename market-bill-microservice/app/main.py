from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.db_connection import db_dependency, engine
from app.infrastructure.database.base import Base
from app.api.v1.endpoints import offers, sales
from contextlib import asynccontextmanager


app = FastAPI()

# Include the routers
app.include_router(offers.router, prefix="/api/v1/offers", tags=["offers"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["sales"])


@app.get("/")
async def welcome(db: AsyncSession = Depends(db_dependency)):
    """
    Welcome endpoint to verify that the API is up and running.

    Args:
        db (AsyncSession): The asynchronous database session provided by the dependency.

    Returns:
        dict: A simple message indicating that the API is up and running.
    """
    return {"message": "Welcome to the User authentication and management API"}
