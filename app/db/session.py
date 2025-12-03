from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker  # (+ AsyncSession if needed)
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Create an async engine (PostgreSQL with asyncpg, or SQLite with aiosqlite)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# Async session factory
SessionLocal = async_sessionmaker[AsyncSession](bind=engine, autoflush=False, expire_on_commit=False)

# Base class for models (same as before)
Base = declarative_base()

# Dependency for FastAPI to get a session
async def get_db():
    db = SessionLocal()  # this gives an AsyncSession
    try:
        yield db
    finally:
        # Close the session after use
        await db.close()
