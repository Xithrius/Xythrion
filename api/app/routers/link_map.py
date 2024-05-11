from fastapi import APIRouter, HTTPException, Response, status

from app.database.crud.link_map_channel import link_map_channel_dao
from app.database.crud.link_map_converter import link_map_converter_dao
from app.database.dependencies import DBSession
from app.database.models.link_map import LinkMapChannelModel, LinkMapConverterModel

from .schemas.link_map import (
    LinkMapChannel,
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
    channels = await link_map_channel_dao.get_all(session)

    return list(channels)


@router.get(
    "/converters/all",
    response_model=list[LinkMapConverter],
    status_code=status.HTTP_200_OK,
)
async def get_all_link_map_converters(session: DBSession) -> list[LinkMapConverterModel]:
    converters = await link_map_converter_dao.get_all(session)

    return list(converters)


@router.get(
    "/channels/{channel_id}",
    response_model=LinkMapChannel,
    status_code=status.HTTP_200_OK,
)
async def get_one_link_map_channel(session: DBSession, channel_id: str) -> LinkMapChannelModel:
    channel = await link_map_channel_dao.get_(session, pk=channel_id)

    if channel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link map channel with ID '{channel_id}' could not be found",
        )

    return channel


@router.get(
    "/converters/{converter_id}",
    response_model=LinkMapConverter,
    status_code=status.HTTP_200_OK,
)
async def get_one_link_map_converter(session: DBSession, converter_id: str) -> LinkMapConverterModel:
    converter = await link_map_converter_dao.get_(session, pk=converter_id)

    if converter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link map converter with ID '{converter_id}' could not be found",
        )

    return converter


@router.get(
    "/server/{discord_server_id}/channels",
    response_model=list[LinkMapChannel],
    status_code=status.HTTP_200_OK,
)
async def get_server_link_map_channels(session: DBSession, discord_server_id: int) -> list[LinkMapChannelModel]:
    channels = await link_map_channel_dao.get_by_server_id(session, server_id=discord_server_id)

    return list(channels)


@router.get(
    "/server/{discord_server_id}/converters",
    response_model=list[LinkMapConverter],
    status_code=status.HTTP_200_OK,
)
async def get_server_link_map_converters(session: DBSession, discord_server_id: int) -> list[LinkMapConverterModel]:
    converters = await link_map_converter_dao.get_by_server_id(session, server_id=discord_server_id)

    return list(converters)


@router.get(
    "/channels/{discord_channel_id}/converters",
    response_model=list[LinkMapConverter],
    status_code=status.HTTP_200_OK,
)
async def get_discord_channel_converters(session: DBSession, discord_channel_id: int) -> list[LinkMapConverterModel]:
    items = await link_map_channel_dao.get_converters_for_channel(
        session,
        input_channel_id=discord_channel_id,
    )

    if (converters := items) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No link map converters for discord channel with ID {discord_channel_id} could be found",
        )

    return converters


@router.post(
    "/channels",
    response_model=LinkMapChannel,
    status_code=status.HTTP_201_CREATED,
)
async def create_link_map_channel(
    session: DBSession,
    link_map_channel: LinkMapChannelCreate,
) -> LinkMapChannelModel:
    channels = await link_map_channel_dao.get_by_server_id(
        session,
        server_id=link_map_channel.server_id,
    )

    if channels:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Link map channel already exists in server with ID '{link_map_channel.server_id}'",
        )

    return await link_map_channel_dao.create(session, obj_in=link_map_channel)


@router.post(
    "/converters",
    response_model=LinkMapConverter,
    status_code=status.HTTP_201_CREATED,
)
async def create_link_map_converter(
    session: DBSession,
    link_map_converter: LinkMapConverterCreate,
) -> LinkMapConverterModel:
    if (link_map_converter.to_link is None) == (link_map_converter.xpath is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only populate `to_link` or `xpath`.",
        )

    converter = await link_map_converter_dao.get_by_link(session, link_map=link_map_converter)

    if converter is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Link map converter already exists",
        )

    return await link_map_converter_dao.create(session, obj_in=link_map_converter)


@router.put(
    "/channels/{channel_id}/converters/{converter_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def enable_link_map_converter_for_channel(
    session: DBSession,
    channel_id: str,
    converter_id: str,
) -> None:
    # Make sure the converter exists
    channel = await link_map_channel_dao.get_(session, pk=channel_id)

    if channel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link map channel with ID '{channel_id}' could not be found",
        )

    # Make sure the channel exists
    converter = await link_map_converter_dao.get_(session, pk=converter_id)

    if converter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link map converter with ID '{converter_id}' could not be found",
        )

    # Add the converter to the channel
    await link_map_channel_dao.add_converter(
        session,
        channel_id=channel_id,
        converter_id=converter_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/channels/{channel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_link_map_channel(session: DBSession, channel_id: str) -> Response:
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
async def remove_link_map_converter(session: DBSession, converter_id: str) -> Response:
    count = await link_map_converter_dao.delete(session, pk=[converter_id])

    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link map converter with ID '{converter_id}' does not exist.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
