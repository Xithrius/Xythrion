from typing import Annotated

from app.routers.command_metric.schemas import CommandMetricCreate
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db_session
from app.database.models.command_metric import CommandMetricModel


class CommandMetricCRUD:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_db_session)]) -> None:
        self.session = session

    async def create_command_metric(self, item: CommandMetricCreate) -> None:
        self.session.add(CommandMetricModel(**item.model_dump()))

    async def get_all_command_metrics(self, limit: int, offset: int) -> list[CommandMetricModel]:
        raw_items = await self.session.execute(
            select(CommandMetricModel).limit(limit).offset(offset),
        )

        return list(raw_items.scalars().fetchall())

    # async def filter(self, name: str | None = None) -> list[CommandMetricModel]:
    #     query = select(CommandMetricModel)
    #     if name:
    #         query = query.where(CommandMetricModel.name == name)
    #     rows = await self.session.execute(query)
    #     return list(rows.scalars().fetchall())
