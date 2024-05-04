from collections.abc import Sequence

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import CRUDBase
from app.database.models.link_map import LinkMapChannelModel, LinkMapConverterModel
from app.routers.schemas.link_map import (
    LinkMapConverter,
    LinkMapConverterBase,
    LinkMapConverterCreate,
    LinkMapConverterUpdate,
)


class LinkMapConverterCRUD(CRUDBase[LinkMapConverterModel, LinkMapConverterCreate, LinkMapConverterUpdate]):
    async def get_all(self, db: AsyncSession) -> Sequence[LinkMapConverterModel]:
        items = await db.execute(select(self.model))

        return items.scalars().all()

    async def get_by_link(self, db: AsyncSession, *, link_map: LinkMapConverterBase) -> LinkMapConverterModel | None:
        items = await db.execute(
            select(self.model).where(
                and_(
                    self.model.from_link == link_map.from_link,
                    or_(
                        self.model.to_link == link_map.to_link,
                        self.model.xpath == link_map.xpath,
                    ),
                ),
            ),
        )

        return items.scalar()

    async def get_by_server_id(self, db: AsyncSession, *, server_id: int) -> Sequence[LinkMapConverter]:
        # TODO: Make sure this works with tests
        items = await db.execute(
            select(self.model).where(self.model.channels.any(LinkMapChannelModel.server_id == server_id)),
        )

        return items.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: LinkMapConverterCreate) -> None:
        await self.create_(db, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, pk: list[str]) -> int:
        return await self.delete_(db, pk=pk)


link_map_converter_dao = LinkMapConverterCRUD(LinkMapConverterModel)
