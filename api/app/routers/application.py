from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from app.routers import api_router
from app.routers.lifetime import lifespan


def get_app() -> FastAPI:
    app = FastAPI(
        title="xythrion-api",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        lifespan=lifespan,
    )

    app.include_router(router=api_router)

    return app
