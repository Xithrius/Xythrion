from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db_session
from app.database.models.web_map import WebMapModel

from .schemas import WebMap

router = APIRouter()


@router.get(
    "/",
    response_model=list[WebMapModel],
    status_code=status.HTTP_200_OK,
)
async def get_web_maps(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    server_id: int,
    user_id: int,
    limit: int | None = 10,
    offset: int | None = 0,
) -> list[WebMapModel]:
    stmt = (
        select(WebMapModel)
        .limit(limit)
        .offset(offset)
        .where(
            (WebMapModel.server_id == server_id) and (WebMapModel.user_id == user_id),
        )
    )

    items = await session.execute(stmt)

    return list(items.scalars().fetchall())


@router.post(
    "/",
    response_model=WebMapModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_web_map(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    web_map: WebMap,
) -> WebMapModel:
    new_item = WebMapModel(**web_map.model_dump())

    session.add(new_item)
    await session.flush()

    return new_item


@router.delete(
    "/{id}",
    response_model=WebMapModel,
    status_code=status.HTTP_200_OK,
)
async def remove_web_map(
    session: Annotated[AsyncSession, Depends(get_db_session)], id: int,
) -> WebMapModel:
    ...
