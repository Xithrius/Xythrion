from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import Select, and_, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import CRUDBase
from app.database.models.command_metric import CommandMetricModel
from app.routers.command_metric.schemas import CommandMetricCreate, CommandMetricUpdate


class CommandMetricCRUD(CRUDBase[CommandMetricModel, CommandMetricCreate, CommandMetricUpdate]):
    async def get(self, db: AsyncSession, *, pk: UUID) -> CommandMetricModel | None:
        return await self.get_(db, pk=pk)

    async def get_list(
        self,
        command_name: str | None = None,
        successfully_completed: bool | None = None,
    ) -> Select:
        se = select(self.model).order_by(desc(self.model.used_at))

        where_list = []

        if command_name:
            where_list.append(self.model.command_name.like(f"%{command_name}%"))
        if successfully_completed is not None:
            where_list.append(self.model.successfully_completed == successfully_completed)

        if where_list:
            se = se.where(and_(*where_list))

        return se

    async def get_all(self, db: AsyncSession, *, limit: int, offset: int) -> Sequence[CommandMetricModel]:
        items = await db.execute(select(self.model).limit(limit).offset(offset))

        return items.scalars().all()

    async def get_by_command_name(self, db: AsyncSession, *, command_name: str) -> CommandMetricModel | None:
        items = await db.execute(select(self.model).where(self.model.command_name == command_name))

        return items.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: CommandMetricCreate) -> CommandMetricModel:
        new_item = await self.create_(db, obj_in=obj_in)

        return new_item

    async def delete(self, db: AsyncSession, *, pk: list[UUID]) -> int:
        items = await db.execute(delete(self.model).where(self.model.id.in_(pk)))

        return items.rowcount


command_metric_dao: CommandMetricCRUD = CommandMetricCRUD(CommandMetricModel)


# class CommandMetricCRUD:
#     def __init__(self, session: Annotated[AsyncSession, Depends(get_db_session)]) -> None:
#         self.session = session

#     async def create_command_metric(self, item: CommandMetricCreate) -> None:
#         self.session.add(CommandMetricModel(**item.model_dump()))

#     async def get_all_command_metrics(self, limit: int, offset: int) -> list[CommandMetricModel]:
#         raw_items = await self.session.execute(
#             select(CommandMetricModel).limit(limit).offset(offset),
#         )

#         return list(raw_items.scalars().fetchall())

# async def filter(self, name: str | None = None) -> list[CommandMetricModel]:
#     query = select(CommandMetricModel)
#     if name:
#         query = query.where(CommandMetricModel.name == name)
#     rows = await self.session.execute(query)
#     return list(rows.scalars().fetchall())
