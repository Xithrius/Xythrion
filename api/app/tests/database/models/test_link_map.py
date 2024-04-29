import pytest
from app.database.models.link_map import LinkMapChannelModel
from app.routers.schemas.link_map import LinkMapChannelCreate
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.anyio
async def test_create_one_link_map_channel_model(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    obj_in = LinkMapChannelCreate(
        server_id=1111,
        input_channel_id=2222,
        output_channel_id=3333,
    )
    create_data = LinkMapChannelModel(**obj_in.model_dump())
    dbsession.add(create_data)


@pytest.mark.anyio
async def test_create_one_link_map_converter_model(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None: ...


@pytest.mark.anyio
async def test_create_one_link_map_to_link_and_xpath_throws_error(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None: ...


@pytest.mark.anyio
async def test_create_one_link_map_no_channel_throws_error(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None: ...
