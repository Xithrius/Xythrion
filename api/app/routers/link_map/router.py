from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db_session
from app.database.models.link_map import LinkMapModel

from .schemas import LinkMap, LinkMapCreate

router = APIRouter()


@router.get(
    "/",
    response_model=list[LinkMap],
    status_code=status.HTTP_200_OK,
)
async def get_link_maps(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    server_id: int,
    user_id: int,
    limit: int | None = 10,
    offset: int | None = 0,
) -> list[LinkMapModel]:
    stmt = (
        select(LinkMapModel)
        .where(
            (LinkMapModel.server_id == server_id) and (LinkMapModel.user_id == user_id),
        )
        .limit(limit)
        .offset(offset)
    )

    items = await session.execute(stmt)

    return list(items.scalars().fetchall())


@router.post(
    "/",
    response_model=LinkMap,
    status_code=status.HTTP_201_CREATED,
)
async def create_link_map(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    link_map: LinkMapCreate,
) -> LinkMapModel:
    new_item = LinkMapModel(**link_map.model_dump())

    session.add(new_item)
    await session.flush()

    return new_item


@router.delete(
    "/{id}",
    response_model=LinkMap,
    status_code=status.HTTP_200_OK,
)
async def remove_link_map(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: int,
) -> LinkMapModel:
    stmt = delete(LinkMapModel).where(LinkMapModel.id == id).returning()

    items = await session.execute(stmt)

    return items
