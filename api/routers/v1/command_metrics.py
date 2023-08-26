from fastapi import APIRouter

from api.database import CommandMetric

router = APIRouter()


@router.post("/command_metrics", response_model=CommandMetric)
async def create_command_ussage_metric(command_metric: CommandMetric) -> CommandMetric:
    return await command_metric.save()
