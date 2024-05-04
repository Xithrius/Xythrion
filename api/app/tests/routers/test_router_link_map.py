import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.anyio
async def test_get_all_link_map_channels_on_empty_database_returns_empty_list(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_all_link_map_channels")
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.anyio
async def test_get_all_link_map_converters_on_empty_database_returns_empty_list(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_all_link_map_converters")
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.anyio
async def test_get_one_link_map_channel_on_empty_database_returns_404_not_found(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "get_one_link_map_channel",
        channel_id="00000000-0000-0000-0000-000000000000",
    )
    response = await client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_get_one_link_map_converter_on_empty_database_returns_404_not_found(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "get_one_link_map_converter",
        converter_id="00000000-0000-0000-0000-000000000000",
    )
    response = await client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_get_server_link_map_channels_on_empty_database_returns_empty_list(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_server_link_map_channels")
    response = await client.get(url, params={"server_id": 1234})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.anyio
async def test_get_server_link_map_converters_on_empty_database_returns_empty_list(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_server_link_map_converters")
    response = await client.get(url, params={"server_id": 1234})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.anyio
async def test_create_link_map_channel_with_valid_data_returns_201_created(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_channel")
    data = {
        "server_id": 1,
        "input_channel_id": 1,
        "output_channel_id": 1,
    }
    response = await client.post(url, json=data)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.anyio
async def test_create_link_map_converter_with_valid_data_returns_201_created(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_converter")
    response = await client.post(
        url,
        json={"from_link": "https://example.com", "to_link": "https://example.com/test"},
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.anyio
async def test_create_link_map_channel_with_duplicate_data_returns_409_conflict(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_channel")
    data = {
        "server_id": 2,
        "input_channel_id": 2,
        "output_channel_id": 2,
    }

    response = await client.post(url, json=data)
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.post(url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.anyio
async def test_create_link_map_converter_with_duplicate_data_returns_409_conflict(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_converter")
    data = {
        "from_link": "https://asdf.com",
        "to_link": "https://asdf.com/test",
    }

    response = await client.post(url, json=data)
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.post(url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.anyio
async def test_remove_link_map_channel_on_empty_database_returns_404_not_found(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "remove_link_map_channel",
        channel_id="00000000-0000-0000-0000-000000000000",
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_remove_link_map_converter_on_non_empty_database_returns_204_no_content(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_converter")
    data = {
        "from_link": "https://1234.com",
        "to_link": "https://4321.com/test",
    }
    response = await client.post(url, json=data)
    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("get_all_link_map_converters")
    response = await client.get(url)

    link_map_converters = response.json()

    assert len(link_map_converters) == 1

    new_link_map_converter = link_map_converters[0]
    assert new_link_map_converter["id"]
    for k, v in data.items():
        assert new_link_map_converter[k] == v

    url = fastapi_app.url_path_for(
        "remove_link_map_converter",
        converter_id=new_link_map_converter["id"],
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.anyio
async def test_remove_link_map_channel_on_non_empty_database_returns_204_no_content(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_channel")
    data = {
        "server_id": 3,
        "input_channel_id": 3,
        "output_channel_id": 3,
    }
    response = await client.post(url, json=data)
    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("get_all_link_map_channels")
    response = await client.get(url)

    link_map_channels = response.json()

    assert len(link_map_channels) == 1

    new_link_map_channel = link_map_channels[0]
    assert new_link_map_channel["id"]
    for k, v in data.items():
        assert new_link_map_channel[k] == v

    url = fastapi_app.url_path_for(
        "remove_link_map_channel",
        channel_id=new_link_map_channel["id"],
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
