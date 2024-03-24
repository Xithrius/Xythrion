from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:  # pragma: no cover
    """Yield a database session, for use with a FastAPI dependency."""
    async with request.app.state.db_session_factory() as session, session.begin():
        yield session


DBSession = Annotated[AsyncSession, Depends(get_db_session)]
