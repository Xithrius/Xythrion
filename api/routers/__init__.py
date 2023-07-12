from fastapi import APIRouter

from api.routers import link_map, ping

api_router = APIRouter()
api_router.include_router(link_map.router)
api_router.include_router(ping.router)
