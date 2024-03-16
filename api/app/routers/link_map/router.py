from app.database.dependencies import DBSession
from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy import select

from app.database.crud.link_map_channel import link_map_channel_dao
from app.database.crud.link_map_converter import link_map_converter_dao
from app.database.models.link_map import LinkMapChannelModel, LinkMapConverterModel

from .schemas import (
    LinkMapChannel,
    LinkMapChannelConverters,
    LinkMapChannelCreate,
    LinkMapConverter,
    LinkMapConverterCreate,
)

router = APIRouter()


@router.get(
    "/channels",
    response_model=list[LinkMapChannel],
    status_code=status.HTTP_200_OK,
)
async def get_all_link_map_channels(
    session: DBSession,
) -> list[LinkMapChannelModel]:
    return await link_map_channel_dao.get_all(session)


@router.get(
    "/channels",
    response_model=LinkMapChannel,
    status_code=status.HTTP_200_OK,
)
async def get_one_link_map_channel(
    session: DBSession,
    server_id: int | None = None,
) -> LinkMapChannelModel:
    channel = await link_map_channel_dao.get_by_server_id(session, server_id=server_id)

    if channel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No link map channels could be found for server with ID '{server_id}'",
        )

    return channel


@router.get(
    "/converters",
    status_code=status.HTTP_200_OK,
)
async def get_all_channel_link_map_converters(
    session: DBSession,
    server_id: int,
    input_channel_id: int,
) -> LinkMapChannelConverters | None:
    stmt = select(LinkMapChannelModel).where(
        LinkMapChannelModel.server_id == server_id,
        LinkMapChannelModel.input_channel_id == input_channel_id,
    )

    items = await session.execute(stmt)
    items.unique()

    return items.scalars().one_or_none()


@router.post(
    "/channels",
    status_code=status.HTTP_201_CREATED,
)
async def create_link_map_channel(
    session: DBSession,
    new_link_map_channel: LinkMapChannelCreate,
) -> None:
    channels = await link_map_channel_dao.get_by_server_id(
        session,
        server_id=new_link_map_channel.server_id,
    )

    if channels is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Link map channel with ID '{new_link_map_channel.server_id}' already exists",
        )

    await link_map_channel_dao.create(session, obj_in=new_link_map_channel)


@router.post(
    "/converters",
    response_model=LinkMapConverter,
    status_code=status.HTTP_201_CREATED,
)
async def create_link_map_converter(
    session: DBSession,
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

    # channel = await link_map_channel_dao.get_by_server_id(session)

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
    "/channels/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_link_map_channel(
    session: DBSession,
    id: str,
) -> None:
    count = await link_map_channel_dao.delete(session, pk=[id])

    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link map channel with ID '{id}' does not exist.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/converters/{id}",
    status_code=status.HTTP_200_OK,
)
async def remove_link_map_converter(
    session: DBSession,
    id: str,
) -> None:
    count = await link_map_converter_dao.delete(session, pk=[id])

    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link map converter with ID '{id}' does not exist.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
