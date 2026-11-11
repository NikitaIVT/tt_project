from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
import src.events


engine: AsyncEngine = create_async_engine(
    str(settings.POSTGRES_URL),
    pool_pre_ping=True,
)

SessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with SessionFactory() as session:
        try:
            yield session
            if not session.sync_session.info.get("clean", True):
                await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
