from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import CRUDBase
from app.database.models.link_map import LinkMapChannelModel
from app.routers.link_map.schemas import LinkMapChannelCreate, LinkMapChannelUpdate


class LinkMapChannelCRUD(CRUDBase[LinkMapChannelModel, LinkMapChannelCreate, LinkMapChannelUpdate]):
    async def get_all(self, db: AsyncSession) -> Sequence[LinkMapChannelModel]:
        items = await db.execute(select(self.model))
        items.unique()

        return items.scalars().all()

    async def get_by_server_id(self, db: AsyncSession, *, server_id: int) -> LinkMapChannelModel | None:
        items = await db.execute(select(self.model).where(self.model.server_id == server_id))

        return items.scalars().first()

    async def get_converters_for_channel(
        self,
        db: AsyncSession,
        *,
        server_id: int,
        input_channel_id: int,
    ) -> LinkMapChannelModel | None:
        items = await db.execute(
            select(LinkMapChannelModel).where(
                LinkMapChannelModel.server_id == server_id,
                LinkMapChannelModel.input_channel_id == input_channel_id,
            ),
        )
        items.unique()

        return items.scalars().one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: LinkMapChannelCreate) -> LinkMapChannelModel:
        await self.create_(db, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, pk: list[int]) -> int:
        return await self.delete_(db, pk=lambda: self.model.server_id.in_(pk))


link_map_channel_dao = LinkMapChannelCRUD(LinkMapChannelModel)
