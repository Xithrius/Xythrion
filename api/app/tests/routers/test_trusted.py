import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


@pytest.mark.anyio
async def test_check_no_trusted_users(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_all_trusted_users")
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == []


@pytest.mark.anyio
async def test_get_single_invalid_trusted_user_throws_404(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_trusted_user", user_id=1234)
    response = await client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_trust_one_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_trusted_user")
    new_trusted_user = {
        "user_id": 1000,
    }
    response = await client.post(url, json=new_trusted_user)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.anyio
async def test_trust_one_user_then_list(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_trusted_user")
    new_trusted_user = {
        "user_id": 1000,
    }
    response = await client.post(url, json=new_trusted_user)
    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("get_all_trusted_users")
    all_trusted_users = await client.get(url)

    assert all_trusted_users.status_code == status.HTTP_200_OK

    assert new_trusted_user["user_id"] == all_trusted_users.json()[0]["user_id"]


@pytest.mark.anyio
async def test_trust_user_twice_creates_conflict(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_trusted_user")
    new_trusted_user = {
        "user_id": 1000,
    }
    response = await client.post(url, json=new_trusted_user)
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.post(url, json=new_trusted_user)
    assert response.status_code == status.HTTP_409_CONFLICT
