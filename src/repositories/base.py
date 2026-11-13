from uuid import UUID

from sqlalchemy import select, update, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Base


class BaseRepository:
    model: None
    excluded_update_fields = {"id", "created_at", "updated_at", "is_deleted"}

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> Sequence[Base]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)

        return res.scalars().all()

    async def get_by_id(self, uuid: UUID) -> Base | None:
        stmt = select(self.model).where(self.model.id == uuid)
        res = await self.session.execute(stmt)

        return res.scalars().one_or_none()

    async def create(self, data: Base) -> Base:
        self.session.add(data)
        await self.session.flush()
        return data

    async def update(self, data: Base) -> Base | None:
        values = {
            col.key: getattr(data, col.key)
            for col in self.model.__table__.columns
            if col.key not in self.excluded_update_fields
        }
        stmt = (
            update(self.model)
            .where(self.model.id == data.id)
            .values(values)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete(self, data: Base) -> Base:
        data.is_deleted = True
        await self.session.flush()
        return data

