from uuid import UUID

from app.database.dependencies import DBSession
from fastapi import APIRouter, HTTPException, Response, status

from app.database.crud.command_metric import command_metric_dao
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
    session: DBSession,
    limit: int | None = 10,
    offset: int | None = 0,
) -> list[CommandMetricModel]:
    return await command_metric_dao.get_all(session, offset=offset, limit=limit)


@router.post(
    "/",
    description="Create a command metric item",
    status_code=status.HTTP_201_CREATED,
)
async def create_command_usage_metric(
    session: DBSession,
    command_metric: CommandMetricCreate,
) -> None:
    await command_metric_dao.create(session, obj_in=command_metric)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_command_usage_metric(
    session: DBSession,
    item_id: UUID,
) -> Response:
    count = await command_metric_dao.delete(session, pk=[item_id])

    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Command metric with ID '{item_id}' does not exist.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
