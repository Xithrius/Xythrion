from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db_session
from app.database.models.command_metric import CommandMetricModel

from .schemas import CommandMetric

router = APIRouter()


@router.post(
    "/",
    response_model=CommandMetricModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_command_usage_metric(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    command_metric: CommandMetric,
) -> CommandMetricModel:
    new_item = CommandMetricModel(**command_metric.model_dump())

    session.add(new_item)
    await session.flush()

    return new_item
