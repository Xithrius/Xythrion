from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import CRUDBase
from app.database.models.link_map import LinkMapChannelModel
from app.routers.link_map.schemas import LinkMapChannelCreate, LinkMapChannelUpdate


class LinkMapChannelCRUD(CRUDBase[LinkMapChannelModel, LinkMapChannelCreate, LinkMapChannelUpdate]):
    async def get(self, db: AsyncSession, *, pk: UUID) -> LinkMapChannelModel | None:
        return await self.get_(db, pk=pk)

    async def get_all(self, db: AsyncSession, *, limit: int, offset: int) -> Sequence[LinkMapChannelModel]:
        items = await db.execute(select(self.model).limit(limit).offset(offset))

        return items.scalars().all()

    async def get_by_command_name(self, db: AsyncSession, *, command_name: str) -> LinkMapChannelModel | None:
        items = await db.execute(select(self.model).where(self.model.command_name == command_name))

        return items.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: LinkMapChannelCreate) -> LinkMapChannelModel:
        new_item = await self.create_(db, obj_in=obj_in)

        return new_item

    async def delete(self, db: AsyncSession, *, pk: list[UUID]) -> int:
        items = await db.execute(delete(self.model).where(self.model.id.in_(pk)))

        return items.rowcount


link_map_channel_dao = LinkMapChannelCRUD(LinkMapChannelModel)