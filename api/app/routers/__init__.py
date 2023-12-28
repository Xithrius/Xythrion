from fastapi import APIRouter

from .command_metric import router as command_metrics_router
from .link_map import router as link_maps_router
from .monitoring import router as monitor_router
from .pin import router as pin_router
from .trusted import router as trusted_router
from .web_map import router as web_maps_router

api_router = APIRouter(prefix="/api")

api_router.include_router(command_metrics_router, prefix="/command_metrics")
api_router.include_router(link_maps_router, prefix="/link_maps")
api_router.include_router(pin_router, prefix="/pins")
api_router.include_router(trusted_router, prefix="/trusted")
api_router.include_router(web_maps_router, prefix="/web_maps")
api_router.include_router(monitor_router)
