from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:
        yield session
    finally:
        await session.commit()
        await session.close()


# async def _get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     """Yield a database session, for use with a FastAPI dependency."""
#     async with Connections.DB_SESSION_MAKER() as session, session.begin():
#         yield session


# DBSession = typing.Annotated[AsyncSession, Depends(_get_db_session)]
