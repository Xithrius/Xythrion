from fastapi import APIRouter
from .command_metrics import router as command_metrics_router

v1 = APIRouter(prefix="/v1")

v1.include_router(command_metrics_router, prefix="/metrics")
