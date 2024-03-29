from fastapi import APIRouter, HTTPException, Response, status

from app.database.crud.link_map_channel import link_map_channel_dao
from app.database.crud.link_map_converter import link_map_converter_dao
from app.database.dependencies import DBSession
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
    "/channels/all",
    response_model=list[LinkMapChannel],
    status_code=status.HTTP_200_OK,
)
async def get_all_link_map_channels(session: DBSession) -> list[LinkMapChannelModel]:
    items = await link_map_channel_dao.get_all(session)

    return list(items)


@router.get(
    "/converters/all",
    response_model=list[LinkMapConverter],
    status_code=status.HTTP_200_OK,
)
async def get_all_link_map_converters(session: DBSession) -> list[LinkMapConverterModel]:
    items = await link_map_converter_dao.get_all(session)

    return list(items)


@router.get(
    "/channels",
    response_model=LinkMapChannel,
    status_code=status.HTTP_200_OK,
)
async def get_one_link_map_channel(
    session: DBSession,
    server_id: int,
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
) -> LinkMapChannelConverters:
    converters = await link_map_channel_dao.get_converters_for_channel(
        session,
        server_id=server_id,
        input_channel_id=input_channel_id,
    )

    return converters or Response(status_code=status.HTTP_204_NO_CONTENT)


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
    status_code=status.HTTP_201_CREATED,
)
async def create_link_map_converter(
    session: DBSession,
    link_map: LinkMapConverterCreate,
) -> None:
    if (link_map.to_link is None) == (link_map.xpath is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only populate `to_link` or `xpath`.",
        )

    channel = await link_map_channel_dao.get_by_server_id(
        session,
        server_id=link_map.channel_map_server_id,
    )

    if channel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Relevant channel map does not exist for server ID '{link_map.channel_map_server_id}'",
        )

    await link_map_converter_dao.create(session, obj_in=link_map)


@router.delete(
    "/channels/{channel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_link_map_channel(
    session: DBSession,
    channel_id: int,
) -> Response:
    count = await link_map_channel_dao.delete(session, pk=[channel_id])

    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link map channel with ID '{channel_id}' does not exist.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/converters/{converter_id}",
    status_code=status.HTTP_200_OK,
)
async def remove_link_map_converter(
    session: DBSession,
    converter_id: str,
) -> Response:
    count = await link_map_converter_dao.delete(session, pk=[converter_id])

    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link map converter with ID '{converter_id}' does not exist.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
