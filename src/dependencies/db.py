from typing import Annotated

from fastapi import Depends

from src.db import SessionFactory
from src.utils.db_manager import DBManager


async def get_db():
    async with DBManager(session_factory=SessionFactory) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
