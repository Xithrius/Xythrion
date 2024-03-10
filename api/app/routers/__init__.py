from fastapi import APIRouter

from .command_metric import router as command_metrics_router
from .link_map import router as link_maps_router
from .monitoring import router as monitor_router
from .pin import router as pin_router
from .trusted import router as trusted_router

api_router = APIRouter(prefix="/api")

api_router.include_router(
    command_metrics_router,
    prefix="/command_metrics",
    tags=["Metrics"],
)
api_router.include_router(link_maps_router, prefix="/link_maps", tags=["Link maps"])
api_router.include_router(pin_router, prefix="/pins", tags=["Pins"])
api_router.include_router(trusted_router, prefix="/trusted", tags=["Trusted"])
api_router.include_router(monitor_router, tags=["Health"])
