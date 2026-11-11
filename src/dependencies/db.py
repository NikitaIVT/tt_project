from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session


async def get_db():
    async with get_session() as session:
        yield session


DBDep = Annotated[AsyncSession, Depends(get_db)]
