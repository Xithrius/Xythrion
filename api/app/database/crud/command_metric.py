from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import CRUDBase
from app.database.models.command_metric import CommandMetricModel
from app.routers.command_metric.schemas import CommandMetricCreate, CommandMetricUpdate


class CommandMetricCRUD(CRUDBase[CommandMetricModel, CommandMetricCreate, CommandMetricUpdate]):
    async def get_all(self, db: AsyncSession, *, limit: int, offset: int) -> Sequence[CommandMetricModel]:
        items = await db.execute(select(self.model).limit(limit).offset(offset))

        return items.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CommandMetricCreate) -> None:
        await self.create_(db, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, pk: list[UUID]) -> int:
        return await self.delete_(db, pk=pk)


command_metric_dao = CommandMetricCRUD(CommandMetricModel)
