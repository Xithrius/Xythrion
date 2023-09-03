from fastapi import APIRouter

from .command_metrics import router as command_metrics_router
from .drg import router as drg_router
from .link_map import router as link_map_router
from .ping import router as ping_router
from .web_map import router as web_map_router

v1 = APIRouter(prefix="/v1")

v1.include_router(command_metrics_router, prefix="/metrics")
v1.include_router(drg_router, prefix="/drg")
v1.include_router(link_map_router, prefix="/link_map")
v1.include_router(ping_router, prefix="/ping")
v1.include_router(web_map_router, prefix="/web_map")
