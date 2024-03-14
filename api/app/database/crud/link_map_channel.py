from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db_session


class LinkMapChannelCRUD:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_db_session)]) -> None:
        self.session = session

    async def create_(self, item: Any) -> None:
        # self.session.add(...(**item.model_dump()))
        ...
