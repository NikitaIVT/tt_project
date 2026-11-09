from pydantic import BaseModel
from sqlalchemy import select, insert, update


class BaseRepository:
    model: None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)

        return res.scalars().all()

    async def create(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump())
        await self.session.execute(stmt)

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        res = await self.session.execute(stmt)
        return res.rowcount

    async def set_is_deleted(self, ids: list[int] | int, is_deleted: bool = True):
        if isinstance(ids, int):
            ids = [ids]

        stmt = (
            update(self.model)
            .where(self.model.id.in_(ids))
            .values(is_deleted=is_deleted)
        )
        res = await self.session.execute(stmt)
        return res.rowcount

