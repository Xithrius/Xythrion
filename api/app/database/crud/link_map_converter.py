from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import CRUDBase
from app.database.models.link_map import LinkMapConverterModel
from app.routers.schemas.link_map import LinkMapConverterCreate, LinkMapConverterUpdate


class LinkMapConverterCRUD(CRUDBase[LinkMapConverterModel, LinkMapConverterCreate, LinkMapConverterUpdate]):
    async def get_all(self, db: AsyncSession) -> Sequence[LinkMapConverterModel]:
        items = await db.execute(select(self.model))

        return items.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: LinkMapConverterCreate) -> None:
        await self.create_(db, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, pk: list[str]) -> int:
        return await self.delete_(db, pk=pk)


link_map_converter_dao = LinkMapConverterCRUD(LinkMapConverterModel)
