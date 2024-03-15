from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.dependencies import get_db_session
from app.database.models.link_map import LinkMapChannelModel, LinkMapConverterModel

from .schemas import LinkMapChannel, LinkMapChannelUpdate, LinkMapConverter, LinkMapConverterCreate

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
    stmt = select(LinkMapChannelModel)

    if server_id is not None:
        stmt = stmt.where(LinkMapChannelModel.server_id == server_id)

    items = await session.execute(stmt)
    items.unique()

    return list(items.scalars().fetchall())


@router.get(
    "/converters",
    response_model=list[LinkMapConverter],
    status_code=status.HTTP_200_OK,
)
async def get_all_link_map_converters(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    server_id: int | None = None,
    input_channel_id: int | None = None,
) -> list[LinkMapConverterModel]:
    stmt = select(LinkMapConverterModel)

    if server_id and input_channel_id:
        stmt = (
            stmt.join(LinkMapChannelModel, LinkMapConverterModel.channel_map)
            .where(
                LinkMapConverterModel.channel_map_server_id == server_id,
                LinkMapChannelModel.input_channel_id == input_channel_id,
            )
            .options(selectinload(LinkMapConverterModel.channel_map))
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
    link_map_channel: LinkMapChannelUpdate,
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
    response_model=LinkMapConverter,
    status_code=status.HTTP_201_CREATED,
)
async def create_link_map_converter(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    link_map: LinkMapConverterCreate,
) -> LinkMapConverterModel:
    if (link_map.to_link is None) == (link_map.xpath is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only populate `to_link` or `xpath`.",
        )

    stmt = select(LinkMapChannelModel).where(
        LinkMapChannelModel.server_id == link_map.channel_map_server_id,
    )

    items = await session.execute(stmt)
    items.unique()

    if items.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Relevant channel map does not exist for server ID '{link_map.channel_map_server_id}'",
        )

    new_item = LinkMapConverterModel(**link_map.model_dump())

    session.add(new_item)
    await session.flush()

    return new_item


@router.delete(
    "/converters/{id}",
    response_model=LinkMapConverter,
    status_code=status.HTTP_200_OK,
)
async def remove_link_map_converter(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: str,
) -> LinkMapConverterModel:
    stmt = select(LinkMapConverterModel).where(LinkMapConverterModel.id == id)

    items = await session.execute(stmt)
    items.unique()

    if (item := items.scalar_one_or_none()) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Converter by ID '{id}' not found",
        )

    stmt = delete(LinkMapConverterModel).where(LinkMapConverterModel.id == id)

    await session.execute(stmt)
    await session.commit()

    return item
