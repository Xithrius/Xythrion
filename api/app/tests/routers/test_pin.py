import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


@pytest.mark.anyio
async def test_pin_listing_when_no_created_returns_empty_list(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_all_pins")
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == []


@pytest.mark.anyio
async def test_pin_create_one_returns_valid_response(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_pin")
    new_pin = {
        "server_id": 1000,
        "channel_id": 2000,
        "message_id": 3000,
        "user_id": 4000,
    }
    response = await client.post(url, json=new_pin)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    created_on = data.pop("created_at")

    assert created_on
    assert data == new_pin


@pytest.mark.anyio
async def test_pin_create_single_can_be_listed(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_pin")
    new_pin = {
        "server_id": 1000,
        "channel_id": 2000,
        "message_id": 3000,
        "user_id": 4000,
    }
    pin_response = await client.post(url, json=new_pin)
    assert pin_response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("get_all_pins")
    all_pins_response = await client.get(url)

    assert all_pins_response.status_code == status.HTTP_200_OK

    assert pin_response.json() == all_pins_response.json()[0]


@pytest.mark.anyio
async def test_pin_create_duplicate_throws_409(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_pin")
    new_pin = {
        "server_id": 1000,
        "channel_id": 2000,
        "message_id": 3000,
        "user_id": 4000,
    }
    response = await client.post(url, json=new_pin)
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.post(url, json=new_pin)
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.anyio
async def test_pin_remove_invalid_throws_404(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "remove_pin",
        server_id=1000,
        channel_id=2000,
        message_id=3000,
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_pin_create_and_delete_single_pin_lists_nothing(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_pin")
    new_pin = {
        "server_id": 1000,
        "channel_id": 2000,
        "message_id": 3000,
        "user_id": 4000,
    }
    response = await client.post(url, json=new_pin)
    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for(
        "remove_pin",
        server_id=1000,
        channel_id=2000,
        message_id=3000,
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_200_OK

    url = fastapi_app.url_path_for("get_all_pins")
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == []
