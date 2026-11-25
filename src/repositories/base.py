from uuid import UUID

from sqlalchemy import select, update, Sequence, inspect
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Base


class BaseRepository:
    model: None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, uuid: UUID) -> Base | None:
        stmt = select(self.model).where(self.model.id == uuid)
        res = await self.session.execute(stmt)

        return res.scalars().one_or_none()

    async def create(self, data: Base) -> Base:
        self.session.add(data)
        await self.session.flush()
        return data

    async def update(self, data: Base) -> Base | None:
        state = inspect(data)

        values = {
            attr.key: getattr(data, attr.key)
            for attr in state.mapper.column_attrs
            if state.attrs[attr.key].history.has_changes()
        }
        if values:
            stmt = (
                update(self.model)
                .where(self.model.id == data.id)
                .values(values)
                .returning(self.model)
            )
            await self.session.execute(stmt)
            return data
        return data

    async def delete(self, data: Base) -> Base:
        data.is_deleted = True
        await self.session.flush()
        return data

