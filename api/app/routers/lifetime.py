from collections.abc import Awaitable, Callable

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.settings import settings


def _setup_db(app: FastAPI) -> None:
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:
    @app.on_event("startup")
    async def _startup() -> None:
        app.middleware_stack = None
        _setup_db(app)
        app.middleware_stack = app.build_middleware_stack()

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:
    @app.on_event("shutdown")
    async def _shutdown() -> None:
        await app.state.db_engine.dispose()

    return _shutdown
