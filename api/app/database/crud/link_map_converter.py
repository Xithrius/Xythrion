from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import CRUDBase
from app.database.models.link_map import LinkMapConverterModel
from app.routers.link_map.schemas import LinkMapConverterCreate, LinkMapConverterUpdate


class LinkMapConverterCRUD(CRUDBase[LinkMapConverterModel, LinkMapConverterCreate, LinkMapConverterUpdate]):
    async def get(self, db: AsyncSession, *, pk: UUID) -> LinkMapConverterModel | None:
        return await self.get_(db, pk=pk)

    async def get_all(self, db: AsyncSession, *, limit: int, offset: int) -> Sequence[LinkMapConverterModel]:
        items = await db.execute(select(self.model).limit(limit).offset(offset))

        return items.scalars().all()

    async def get_by_server_id(self, db: AsyncSession, *, server_id: str) -> Sequence[LinkMapConverterModel]:
        items = await db.execute(select(self.model).where(self.model.channel_map_server_id == server_id))

        return items.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: LinkMapConverterCreate) -> LinkMapConverterModel:
        await self.create_(db, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, pk: list[UUID]) -> int:
        return await self.delete_(db, pk=pk)


link_map_converter_dao = LinkMapConverterCRUD(LinkMapConverterModel)
