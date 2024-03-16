from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.crud.link_map_channel import link_map_channel_dao
from app.database.dependencies import get_db_session
from app.database.models.link_map import LinkMapChannelModel, LinkMapConverterModel

from .schemas import LinkMapChannel, LinkMapChannelCreate, LinkMapConverter, LinkMapConverterCreate

router = APIRouter()


@router.get(
    "/channels",
    response_model=list[LinkMapChannel],
    status_code=status.HTTP_200_OK,
)
async def get_all_link_map_channels(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[LinkMapChannelModel]:
    items = await link_map_channel_dao.get_all(session)

    return list(items)


@router.get(
    "/channels",
    response_model=LinkMapChannel,
    status_code=status.HTTP_200_OK,
)
async def get_one_link_map_channel(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    server_id: int | None = None,
) -> LinkMapChannelModel:
    server_channels = await link_map_channel_dao.get_by_server_id(
        session,
        server_id=server_id,
    )

    if server_channels is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No link map channels could be found for server with ID '{server_id}'",
        )

    return list(server_channels.scalars().fetchall())


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
    status_code=status.HTTP_201_CREATED,
)
async def create_link_map_channel(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    new_link_map_channel: LinkMapChannelCreate,
) -> None:
    server_channels = await link_map_channel_dao.get_by_server_id(
        session,
        server_id=new_link_map_channel.server_id,
    )

    if server_channels is not None:
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
    "/channels/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_link_map_channel(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: str,
) -> None:
    count = await link_map_channel_dao.delete(session, pk=[id])

    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Command metric with ID '{id}' does not exist.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
