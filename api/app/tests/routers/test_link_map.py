import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


@pytest.mark.anyio
async def test_check_no_link_map_channels(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_all_link_map_channels")
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == []


@pytest.mark.anyio
async def test_check_no_link_map_converters(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_all_link_map_converters")
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == []


@pytest.mark.anyio
async def test_create_invalid_link_map_converter_with_no_channels(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_converter")
    new_link_map = {
        "channel_map_server_id": 1000,
        "from_link": "http://example.com",
        "to_link": "http://example.com/example",
        "xpath": "/",
    }
    response = await client.post(url, json=new_link_map)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_create_valid_link_map_channel_and_list(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_channel")
    new_link_map_channel = {
        "server_id": 1,
        "input_channel_id": 2,
        "output_channel_id": 3,
    }
    response = await client.post(url, json=new_link_map_channel)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data.pop("created_at")
    assert data == new_link_map_channel


@pytest.mark.anyio
async def test_create_two_same_link_map_channel_causes_conflict(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_channel")
    new_link_map_channel = {
        "server_id": 2,
        "input_channel_id": 2,
        "output_channel_id": 2,
    }

    response = await client.post(url, json=new_link_map_channel)
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.post(url, json=new_link_map_channel)
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.anyio
async def test_create_valid_channel_and_then_valid_link_map_converter(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_channel")
    new_link_map_channel = {
        "server_id": 1234,
        "input_channel_id": 1234,
        "output_channel_id": 1234,
    }
    response = await client.post(url, json=new_link_map_channel)

    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("create_link_map_converter")
    new_link_map = {
        "channel_map_server_id": 1234,
        "from_link": "http://example.com",
        "to_link": "http://example.com/example",
    }
    response = await client.post(url, json=new_link_map)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data.pop("id")
    assert data.pop("created_at")

    assert data.pop("xpath") is None
    assert data == new_link_map


@pytest.mark.anyio
async def test_create_valid_channel_and_converter_and_search_with_input_channel(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_channel")
    new_link_map_channel = {
        "server_id": 1111,
        "input_channel_id": 2222,
        "output_channel_id": 3333,
    }
    response = await client.post(url, json=new_link_map_channel)

    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("create_link_map_converter")
    new_link_map = {
        "channel_map_server_id": 1111,
        "from_link": "http://example.com",
        "to_link": "http://example.com/example",
        "xpath": "/",
    }
    response = await client.post(url, json=new_link_map)

    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("get_all_link_map_converters")
    response = await client.get(
        url,
        params={"server_id": 1111, "input_channel_id": 2222},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 1

    d = data[0]

    assert d.pop("id")
    assert d.pop("created_at")

    assert d == new_link_map
