from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.dependencies import get_db_session
from app.database.models.link_map import LinkMapChannelModel, LinkMapModel

from .schemas import LinkMap, LinkMapChannel, LinkMapChannelCreate, LinkMapCreate

router = APIRouter()


@router.get(
    "/channels",
    response_model=list[LinkMapChannel],
    status_code=status.HTTP_200_OK,
)
async def get_all_link_map_channels(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    server_id: int | None = None,
) -> list[LinkMapChannelModel]:
    stmt = select(LinkMapChannelModel).where(LinkMapChannelModel.server_id == server_id)

    items = await session.execute(stmt)
    items.unique()

    return list(items.scalars().fetchall())


@router.get(
    "/converters",
    response_model=list[LinkMap],
    status_code=status.HTTP_200_OK,
)
async def get_all_link_map_converters(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    server_id: int | None = None,
    input_channel_id: int | None = None,
) -> list[LinkMapModel]:
    stmt = (
        select(LinkMapModel)
        .join(LinkMapChannelModel, LinkMapModel.channel_map)
        .where(
            LinkMapModel.channel_map_server_id == server_id,
            LinkMapChannelModel.input_channel_id == input_channel_id,
        )
        .options(selectinload(LinkMapModel.channel_map))
    )

    items = await session.execute(stmt)
    items.unique()

    return list(items.scalars().fetchall())


@router.post(
    "/channels",
    response_model=LinkMapChannel,
    status_code=status.HTTP_201_CREATED,
)
async def create_link_map_channel(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    link_map_channel: LinkMapChannelCreate,
) -> LinkMapChannelModel:
    stmt = select(LinkMapChannelModel).where(
        LinkMapChannelModel.server_id == link_map_channel.server_id,
    )

    items = await session.execute(stmt)
    items.unique()

    if items.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Link map channel with ID '{link_map_channel.server_id}' already exists",
        )

    new_item = LinkMapChannelModel(**link_map_channel.model_dump())

    session.add(new_item)
    await session.flush()

    return new_item


@router.post(
    "/converters",
    response_model=LinkMap,
    status_code=status.HTTP_201_CREATED,
)
async def create_link_map_converter(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    link_map: LinkMapCreate,
) -> LinkMapModel:
    if (link_map.to_link is None) == (link_map.xpath is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only populate `to_link` or `xpath`.",
        )

    stmt = select(LinkMapChannelModel).where(LinkMapChannelModel.server_id == link_map.channel_map_server_id)

    items = await session.execute(stmt)
    items.unique()

    if items.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Relevant channel map does not exist for server ID '{link_map.channel_map_server_id}'",
        )

    new_item = LinkMapModel(**link_map.model_dump())

    session.add(new_item)
    await session.flush()

    return new_item


# @router.delete(
#     "/{id}",
#     response_model=LinkMap,
#     status_code=status.HTTP_200_OK,
# )
# async def remove_link_map(
#     session: Annotated[AsyncSession, Depends(get_db_session)],
#     id: int,
# ) -> LinkMapModel:
#     stmt = delete(LinkMapModel).where(LinkMapModel.id == id).returning()

#     items = await session.execute(stmt)

#     return items
