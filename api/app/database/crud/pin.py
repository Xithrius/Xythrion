from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import ColumnElement, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import CRUDBase
from app.database.models.pin import PinModel
from app.routers.pin.schemas import PinBase, PinCreate, PinUpdate

PinType = TypeVar("PinType", bound=PinBase)


def equivalent_pin_model(pin: Generic[PinType]) -> ColumnElement[bool]:
    return and_(
        PinModel.server_id == pin.server_id,
        PinModel.channel_id == pin.channel_id,
        PinModel.message_id == pin.message_id,
    )


class PinCRUD(CRUDBase[PinModel, PinCreate, PinUpdate]):
    async def get_all(self, db: AsyncSession, *, limit: int, offset: int) -> Sequence[PinModel]:
        items = await db.execute(select(self.model).limit(limit).offset(offset))

        return items.scalars().all()

    async def get_by_section_ids(self, db: AsyncSession, *, pin: PinCreate) -> PinModel | None:
        items = await db.execute(select(self.model).where(equivalent_pin_model(pin)))

        return items.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: PinCreate) -> None:
        await self.create_(db, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, pin: PinBase) -> int:
        return await self.delete_(db, pk=lambda: equivalent_pin_model(pin))


pin_dao = PinCRUD(PinModel)
