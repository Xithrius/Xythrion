from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.database.crud.command_metric import CommandMetricCRUD
from app.database.models.command_metric import CommandMetricModel

from .schemas import CommandMetric, CommandMetricCreate

router = APIRouter()


@router.get(
    "/",
    description="All the command metrics you could ever want",
    response_model=list[CommandMetric],
    status_code=status.HTTP_200_OK,
)
async def get_all_command_metrics(
    crud: Annotated[CommandMetricCRUD, Depends()],
    limit: int | None = 10,
    offset: int | None = 0,
) -> list[CommandMetricModel]:
    return await crud.get_all_command_metrics(limit=limit, offset=offset)


@router.post(
    "/",
    description="Create a command metric item",
    response_model=CommandMetric,
    status_code=status.HTTP_201_CREATED,
)
async def create_command_usage_metric(
    command_metric: CommandMetricCreate,
    crud: Annotated[CommandMetricCRUD, Depends()],
) -> CommandMetricModel:
    return await crud.create_command_metric(command_metric)
