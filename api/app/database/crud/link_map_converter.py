from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import delete, select
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

    async def get_by_command_name(self, db: AsyncSession, *, command_name: str) -> LinkMapConverterModel | None:
        items = await db.execute(select(self.model).where(self.model.command_name == command_name))

        return items.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: LinkMapConverterCreate) -> LinkMapConverterModel:
        new_item = await self.create_(db, obj_in=obj_in)

        return new_item

    async def delete(self, db: AsyncSession, *, pk: list[UUID]) -> int:
        items = await db.execute(delete(self.model).where(self.model.id.in_(pk)))

        return items.rowcount


link_map_converter_dao = LinkMapConverterCRUD(LinkMapConverterModel)
