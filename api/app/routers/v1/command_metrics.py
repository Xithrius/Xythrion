from fastapi import APIRouter, status

from app.database import CommandMetric

router = APIRouter()


@router.post(
    "/command_metric",
    response_model=CommandMetric,
    status_code=status.HTTP_201_CREATED,
)
async def create_command_usage_metric(command_metric: CommandMetric) -> CommandMetric:
    return await command_metric.save()
