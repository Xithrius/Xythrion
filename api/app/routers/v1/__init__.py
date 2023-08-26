from fastapi import APIRouter

from .command_metrics import router as command_metrics_router
from .link_map import router as link_map_router
from .ping import router as ping_router

v1 = APIRouter(prefix="/v1")

v1.include_router(command_metrics_router, prefix="/metrics")
v1.include_router(link_map_router, prefix="/link_map")
v1.include_router(ping_router, prefix="/ping")
