import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


@pytest.mark.anyio
async def test_command_metric_lists_nothing(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_all_command_metrics")
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == []


@pytest.mark.anyio
async def test_command_metric_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_command_usage_metric")
    new_command = {
        "command_name": "test_command",
        "successfully_completed": True,
    }
    response = await client.post(url, json=new_command)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.anyio
async def test_command_metric_creation_and_list(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_command_usage_metric")
    new_command = {
        "command_name": "test_command",
        "successfully_completed": True,
    }
    response = await client.post(url, json=new_command)
    assert response.status_code == status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("get_all_command_metrics")
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 1

    d = data[0]

    command_id = d.pop("id")
    used_at = d.pop("used_at")

    assert command_id
    assert used_at

    assert d == new_command
