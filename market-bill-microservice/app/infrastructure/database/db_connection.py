from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.base import Base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.config import settings

# Define the database URL based on the settings configuration.
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create an asynchronous database engine with the specified database URL.
# `echo=True` enables SQL logging for debugging purposes.
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create an asynchronous session maker bound to the engine.
# This session maker is used to generate new database sessions.
# `autocommit=False` ensures that transactions are managed manually.
# `autoflush=False` disables automatic flushing of the session.
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.

    This function yields a new database session for each request and closes the session when the request is done.
    It also ensures that the database schema is created or updated during startup.

    Returns:
        AsyncGenerator[AsyncSession, None]: An asynchronous generator yielding the database session.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        yield db

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
    """


db_dependency = get_db
