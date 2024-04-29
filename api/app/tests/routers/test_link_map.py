import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


@pytest.mark.anyio
async def test_check_no_link_map_channels_on_invalid_server(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_one_link_map_channel")
    response = await client.get(url, params={"server_id": 1234})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_create_invalid_link_map_converter_with_no_channels(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_converter")
    new_link_map = {
        "channel_map_id": 1000,
        "from_link": "http://example.com",
        "to_link": "http://example.com/example",
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

    url = fastapi_app.url_path_for("get_one_link_map_channel")

    response = await client.get(url, params={"server_id": 1})

    channel = response.json()

    assert channel.pop("created_at")
    assert new_link_map_channel == channel


@pytest.mark.anyio
async def test_create_valid_link_map_channel_and_delete(
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

    url = fastapi_app.url_path_for(
        "remove_link_map_channel",
        channel_id=1,
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


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
async def test_create_valid_channel_but_invalid_converter_with_link_and_xpath(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_channel")
    new_link_map_channel = {
        "server_id": 123,
        "input_channel_id": 123,
        "output_channel_id": 123,
    }
    response = await client.post(url, json=new_link_map_channel)

    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("create_link_map_converter")
    new_link_map = {
        "channel_map_id": 123,
        "from_link": "http://example.com",
        "to_link": "http://example.com/example",
        "xpath": "/",
    }
    response = await client.post(url, json=new_link_map)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_create_valid_channel_but_invalid_converter_with_no_link_and_no_xpath(
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

    url = fastapi_app.url_path_for("create_link_map_converter")
    new_link_map = {
        "channel_map_id": 1,
        "from_link": "http://example.com",
    }
    response = await client.post(url, json=new_link_map)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


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
        "channel_map_id": 1234,
        "from_link": "http://example.com",
        "to_link": "http://example.com/example",
    }
    response = await client.post(url, json=new_link_map)

    assert response.status_code == status.HTTP_201_CREATED


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
        "channel_map_id": 1111,
        "from_link": "http://example.com",
        "to_link": "http://example.com/example",
    }
    response = await client.post(url, json=new_link_map)

    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("get_all_channel_link_map_converters")
    response = await client.get(
        url,
        params={"server_id": 1111, "input_channel_id": 2222},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data["link_maps"]) == 1

    d = data["link_maps"][0]

    assert d.pop("id")
    assert d.pop("created_at")
    assert d.pop("xpath") is None

    # TODO: Attributes

    assert d == new_link_map


@pytest.mark.anyio
async def test_create_valid_channel_and_converter_then_delete_converter_then_list_nothing(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_channel")
    new_link_map_channel = {
        "server_id": 321,
        "input_channel_id": 321,
        "output_channel_id": 321,
    }
    response = await client.post(url, json=new_link_map_channel)

    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("create_link_map_converter")
    new_link_map = {
        "channel_map_id": 321,
        "from_link": "http://example.com",
        "to_link": "http://example.com/example",
    }
    response = await client.post(url, json=new_link_map)

    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("get_all_channel_link_map_converters")
    response = await client.get(
        url,
        params={"server_id": 321, "input_channel_id": 321},
    )

    new_converter = response.json()["link_maps"][0]

    url = fastapi_app.url_path_for("remove_link_map_converter", converter_id=new_converter["id"])
    response = await client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    url = fastapi_app.url_path_for("get_all_channel_link_map_converters")
    response = await client.get(
        url,
        params={"server_id": 321, "input_channel_id": 321},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["link_maps"] == []


@pytest.mark.anyio
async def test_delete_invalid_link_map_channel(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "remove_link_map_channel",
        channel_id=55555,
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_delete_invalid_link_map_converter(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "remove_link_map_converter",
        converter_id="3e552f84-ebeb-4afc-b5db-997abe6d9458",
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
