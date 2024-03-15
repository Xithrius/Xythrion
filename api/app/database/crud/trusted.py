from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import CRUDBase
from app.database.models.trusted import TrustedModel
from app.routers.trusted.schemas import TrustedCreate, TrustedUpdate


class TrustedCRUD(CRUDBase[TrustedModel, TrustedCreate, TrustedUpdate]):
    async def get(self, db: AsyncSession, *, pk: UUID) -> TrustedModel | None:
        return await self.get_(db, pk=pk)

    async def get_all(self, db: AsyncSession, *, limit: int, offset: int) -> Sequence[TrustedModel]:
        items = await db.execute(select(self.model).limit(limit).offset(offset))

        return items.scalars().all()

    # async def get_by_command_name(self, db: AsyncSession, *, command_name: str) -> TrustedModel | None:
    #     items = await db.execute(select(self.model).where(self.model.command_name == command_name))

    #     return items.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: TrustedCreate) -> TrustedModel:
        new_item = await self.create_(db, obj_in=obj_in)

        return new_item

    async def delete(self, db: AsyncSession, *, pk: list[UUID]) -> int:
        items = await db.execute(delete(self.model).where(self.model.id.in_(pk)))

        return items.rowcount


trusted_dao = TrustedCRUD(TrustedModel)
