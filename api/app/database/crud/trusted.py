from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import CRUDBase
from app.database.models.trusted import TrustedModel
from app.routers.trusted.schemas import TrustedCreate, TrustedUpdate


class TrustedCRUD(CRUDBase[TrustedModel, TrustedCreate, TrustedUpdate]):
    async def get_all(self, db: AsyncSession, *, limit: int, offset: int) -> Sequence[TrustedModel]:
        items = await db.execute(select(self.model).limit(limit).offset(offset))

        return items.scalars().all()

    async def get_by_user_id(self, db: AsyncSession, *, user_id: int) -> TrustedModel | None:
        items = await db.execute(select(self.model).where(self.model.user_id == user_id))

        return items.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: TrustedCreate) -> None:
        await self.create_(db, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, pk: list[int]) -> int:
        return await self.delete_(db, pk=lambda: self.model.user_id.in_(pk))


trusted_dao = TrustedCRUD(TrustedModel)
