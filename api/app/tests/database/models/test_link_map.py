import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.anyio
async def test_create_one_link_map_channel_model(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None: ...


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
