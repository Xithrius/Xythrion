from fastapi import APIRouter

from .command_metrics import router as command_metrics_router
from .drg import router as drg_builds_router
from .link_map import router as link_maps_router
from .ping import router as ping_router
from .state import router as state_router
from .web_map import router as web_maps_router

v1 = APIRouter(prefix="/v1")

v1.include_router(command_metrics_router, prefix="/command_metrics")
v1.include_router(drg_builds_router, prefix="/drg_builds")
v1.include_router(link_maps_router, prefix="/link_maps")
v1.include_router(ping_router, prefix="/ping")
v1.include_router(state_router, prefix="/state")
v1.include_router(web_maps_router, prefix="/web_maps")
