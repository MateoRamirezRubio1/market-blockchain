from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.db_connection import db_dependency, engine
from app.infrastructure.database.base import Base
from app.api.v1.endpoints import offers, sales
from contextlib import asynccontextmanager
from app.infrastructure.database.scheduler import scheduler_inicializer
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los origenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Include the routers
app.include_router(offers.router, prefix="/api/v1/offers", tags=["offers"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["sales"])


@app.on_event("startup")
async def iniciar_app():
    scheduler_inicializer()


@app.get("/")
async def welcome(db: AsyncSession = Depends(db_dependency)):
    """
    Welcome endpoint to verify that the API is up and running.

    Args:
        db (AsyncSession): The asynchronous database session provided by the dependency.

    Returns:
        dict: A simple message indicating that the API is up and running.
    """
    return {"message": "Welcome to the Market Bill Microservices API"}
