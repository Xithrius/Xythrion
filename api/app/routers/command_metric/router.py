from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db_session
from app.database.models.command_metric import CommandMetricModel

from .schemas import CommandMetric, CommandMetricCreate

router = APIRouter()


@router.get(
    "/",
    response_model=list[CommandMetric],
    status_code=status.HTTP_200_OK,
)
async def get_all_builds(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int | None = 10,
    offset: int | None = 0,
) -> list[CommandMetricModel]:
    stmt = select(CommandMetricModel).limit(limit).offset(offset)

    items = await session.execute(stmt)

    return list(items.scalars().fetchall())


@router.post(
    "/",
    response_model=CommandMetric,
    status_code=status.HTTP_201_CREATED,
)
async def create_command_usage_metric(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    command_metric: CommandMetricCreate,
) -> CommandMetricModel:
    new_item = CommandMetricModel(**command_metric.model_dump())

    session.add(new_item)
    await session.flush()

    return new_item
