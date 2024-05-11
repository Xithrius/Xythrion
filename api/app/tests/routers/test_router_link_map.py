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
    url = fastapi_app.url_path_for(
        "get_server_link_map_channels",
        discord_server_id=1234,
    )
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.anyio
async def test_get_server_link_map_converters_on_empty_database_returns_empty_list(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "get_server_link_map_converters",
        discord_server_id=1234,
    )
    response = await client.get(url)

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
    data = {
        "from_link": "https://example.com",
        "to_link": "https://example.com/test",
    }
    response = await client.post(url, json=data)

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
async def test_create_link_map_converter_with_xpath_and_to_link_returns_400_bad_request(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_converter")
    data = {
        "from_link": "https://asdf.com",
        "to_link": "https://asdf.com/test",
        "xpath": "/html/body/div",
    }

    response = await client.post(url, json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_get_one_link_map_channel_on_non_empty_database_returns_200_ok(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_link_map_channel")
    data = {
        "server_id": 1000,
        "input_channel_id": 1000,
        "output_channel_id": 1000,
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
        "get_one_link_map_channel",
        channel_id=new_link_map_channel["id"],
    )
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    one_link_map_channel = response.json()

    assert one_link_map_channel == new_link_map_channel


@pytest.mark.anyio
async def test_get_one_link_map_converter_on_non_empty_database_returns_200_ok(
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
        "get_one_link_map_converter",
        converter_id=new_link_map_converter["id"],
    )
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    one_link_map_converter = response.json()

    assert one_link_map_converter == new_link_map_converter


@pytest.mark.anyio
async def test_enable_link_map_converter_for_channel_on_invalid_channel_returns_404_not_found(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "enable_link_map_converter_for_channel",
        channel_id="00000000-0000-0000-0000-000000000000",
        converter_id="00000000-0000-0000-0000-000000000000",
    )
    response = await client.put(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_enable_link_map_converter_for_channel_on_invalid_converter_returns_404_not_found(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    # Create the channel
    url = fastapi_app.url_path_for("create_link_map_channel")
    new_link_map_channel_data = {
        "server_id": 1,
        "input_channel_id": 2,
        "output_channel_id": 3,
    }
    response = await client.post(url, json=new_link_map_channel_data)
    new_link_map_channel = response.json()
    assert new_link_map_channel["id"]

    url = fastapi_app.url_path_for(
        "enable_link_map_converter_for_channel",
        channel_id=new_link_map_channel["id"],
        converter_id="00000000-0000-0000-0000-000000000000",
    )
    response = await client.put(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_enable_link_map_converter_for_channel_returns_204_no_content(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    # Create the channel
    url = fastapi_app.url_path_for("create_link_map_channel")
    new_link_map_channel_data = {
        "server_id": 1,
        "input_channel_id": 1,
        "output_channel_id": 1,
    }
    response = await client.post(url, json=new_link_map_channel_data)
    new_link_map_channel = response.json()
    assert new_link_map_channel["id"]

    # Create the converter
    url = fastapi_app.url_path_for("create_link_map_converter")
    new_link_map_converter_data = {
        "from_link": "https://example.com",
        "to_link": "https://example.com/test",
    }
    response = await client.post(url, json=new_link_map_converter_data)
    new_link_map_converter = response.json()
    assert new_link_map_converter["id"]

    # Add converter to channel
    url = fastapi_app.url_path_for(
        "enable_link_map_converter_for_channel",
        channel_id=new_link_map_channel["id"],
        converter_id=new_link_map_converter["id"],
    )
    response = await client.put(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.anyio
async def test_get_discord_channel_converters_on_empty_db_returns_404_not_found(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "get_discord_channel_converters",
        discord_channel_id=1234,
    )
    response = await client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_get_discord_channel_converters_after_enabled_converter_on_channel_returns_200_ok(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    # Create the channel
    url = fastapi_app.url_path_for("create_link_map_channel")
    new_link_map_channel_data = {
        "server_id": 1,
        "input_channel_id": 2,
        "output_channel_id": 3,
    }
    response = await client.post(url, json=new_link_map_channel_data)
    new_link_map_channel = response.json()
    assert new_link_map_channel["id"]

    # Create the converter
    url = fastapi_app.url_path_for("create_link_map_converter")
    new_link_map_converter_data = {
        "from_link": "https://example.com",
        "to_link": "https://example.com/test",
    }
    response = await client.post(url, json=new_link_map_converter_data)
    new_link_map_converter = response.json()
    assert new_link_map_converter["id"]

    # Add converter to channel
    url = fastapi_app.url_path_for(
        "enable_link_map_converter_for_channel",
        channel_id=new_link_map_channel["id"],
        converter_id=new_link_map_converter["id"],
    )
    response = await client.put(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    url = fastapi_app.url_path_for(
        "get_discord_channel_converters",
        discord_channel_id=2,
    )
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK

    enabled_link_maps = response.json()

    assert len(enabled_link_maps) == 1

    assert enabled_link_maps[0] == new_link_map_converter


@pytest.mark.anyio
async def test_disable_link_map_converter_for_channel_on_invalid_channel_returns_404_not_found(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "disable_link_map_converter_for_channel",
        channel_id="00000000-0000-0000-0000-000000000000",
        converter_id="00000000-0000-0000-0000-000000000000",
    )
    response = await client.put(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_disable_link_map_converter_for_channel_on_invalid_converter_returns_404_not_found(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    # Create the channel
    url = fastapi_app.url_path_for("create_link_map_channel")
    new_link_map_channel_data = {
        "server_id": 1,
        "input_channel_id": 2,
        "output_channel_id": 3,
    }
    response = await client.post(url, json=new_link_map_channel_data)
    new_link_map_channel = response.json()
    assert new_link_map_channel["id"]

    url = fastapi_app.url_path_for(
        "disable_link_map_converter_for_channel",
        channel_id=new_link_map_channel["id"],
        converter_id="00000000-0000-0000-0000-000000000000",
    )
    response = await client.put(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_disable_link_map_converter_for_channel_returns_204_no_content(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    # Create the channel
    url = fastapi_app.url_path_for("create_link_map_channel")
    new_link_map_channel_data = {
        "server_id": 1,
        "input_channel_id": 1,
        "output_channel_id": 1,
    }
    response = await client.post(url, json=new_link_map_channel_data)
    new_link_map_channel = response.json()
    assert new_link_map_channel["id"]

    # Create the converter
    url = fastapi_app.url_path_for("create_link_map_converter")
    new_link_map_converter_data = {
        "from_link": "https://example.com",
        "to_link": "https://example.com/test",
    }
    response = await client.post(url, json=new_link_map_converter_data)
    new_link_map_converter = response.json()
    assert new_link_map_converter["id"]

    # Add converter to channel
    url = fastapi_app.url_path_for(
        "enable_link_map_converter_for_channel",
        channel_id=new_link_map_channel["id"],
        converter_id=new_link_map_converter["id"],
    )
    response = await client.put(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Remove converter from channel
    url = fastapi_app.url_path_for(
        "disable_link_map_converter_for_channel",
        channel_id=new_link_map_channel["id"],
        converter_id=new_link_map_converter["id"],
    )
    response = await client.put(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.anyio
async def test_remove_link_map_converter_on_empty_database_returns_404_not_found(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "remove_link_map_converter",
        converter_id="00000000-0000-0000-0000-000000000000",
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


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

    new_link_map_converter = response.json()

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

    new_link_map_channel = response.json()

    url = fastapi_app.url_path_for(
        "remove_link_map_channel",
        channel_id=new_link_map_channel["id"],
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
