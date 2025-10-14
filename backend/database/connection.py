"""Database connection management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config.settings import settings

# Convert postgresql:// to postgresql+asyncpg://
async_db_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine
engine = create_async_engine(
    async_db_url,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session.

    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
