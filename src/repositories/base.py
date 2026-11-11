from uuid import UUID


from sqlalchemy import select, update, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Base


class BaseRepository:
    model: None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> Sequence[Base]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)

        return res.scalars().all()

    async def get_by_uuid(self, uuid: UUID) -> Base | None:
        stmt = select(self.model).where(self.model.id == uuid)
        res = await self.session.execute(stmt)

        return res.scalars().one_or_none()

    async def create(self, data: Base) -> Base:
        self.session.add(data)
        await self.session.flush()
        return data

    async def update(self, data: Base) -> Base:
        await self.session.flush()
        return data

    async def set_is_deleted(self, ids: list[UUID] | UUID, is_deleted: bool = True):
        if isinstance(ids, int):
            ids = [ids]

        stmt = (
            update(self.model)
            .where(self.model.id.in_(ids))
            .values(is_deleted=is_deleted)
        )
        res = await self.session.execute(stmt)
        return res.rowcount

