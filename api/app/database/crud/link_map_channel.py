from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import CRUDBase
from app.database.models.link_map import LinkMapChannelModel, LinkMapConverterModel
from app.routers.schemas.link_map import LinkMapChannelCreate, LinkMapChannelUpdate


class LinkMapChannelCRUD(CRUDBase[LinkMapChannelModel, LinkMapChannelCreate, LinkMapChannelUpdate]):
    async def get_all(self, db: AsyncSession) -> Sequence[LinkMapChannelModel]:
        items = await db.execute(select(self.model))
        items.unique()

        return items.scalars().all()

    async def get_by_server_id(self, db: AsyncSession, *, server_id: int) -> Sequence[LinkMapChannelModel]:
        items = await db.execute(select(self.model).where(self.model.server_id == server_id))
        items.unique()

        return items.scalars().all()

    async def get_converters_for_channel(
        self,
        db: AsyncSession,
        *,
        input_channel_id: int,
    ) -> list[LinkMapConverterModel] | None:
        items = await db.execute(select(self.model).where(self.model.input_channel_id == input_channel_id))
        items.unique()

        if (channel_converters := items.scalars().first()) is not None:
            return channel_converters.converters

        return None

    async def create(self, db: AsyncSession, *, obj_in: LinkMapChannelCreate) -> LinkMapChannelModel:
        return await self.create_(db, obj_in=obj_in)

    async def add_converter(self, db: AsyncSession, *, channel_id: str, converter_id: str) -> None:
        # Assuming that the channel and converter were already checked to exist beforehand

        channel_results = await db.execute(select(self.model).where(self.model.id == channel_id))
        channel = channel_results.scalars().first()

        converter_results = await db.execute(
            select(LinkMapConverterModel).where(LinkMapConverterModel.id == converter_id),
        )
        converter = converter_results.scalars().first()

        channel.converters.append(converter)

    async def remove_converter(self, db: AsyncSession, *, channel_id: str, converter_id: str) -> None:
        # Assuming that the channel and converter were already checked to exist beforehand

        channel_results = await db.execute(select(self.model).where(self.model.id == channel_id))
        channel = channel_results.scalars().first()

        converter_results = await db.execute(
            select(LinkMapConverterModel).where(LinkMapConverterModel.id == converter_id),
        )
        converter = converter_results.scalars().first()

        channel.converters.remove(converter)

    async def delete(self, db: AsyncSession, *, pk: list[int] | list[str]) -> int:
        return await self.delete_(db, pk=lambda: self.model.id.in_(pk))


link_map_channel_dao = LinkMapChannelCRUD(LinkMapChannelModel)
