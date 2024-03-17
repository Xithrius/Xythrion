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


@pytest.mark.anyio
async def test_command_metric_creation_and_deletion(
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
    d = response.json()[0]

    command_id = d.pop("id")

    url = fastapi_app.url_path_for(
        "remove_command_usage_metric",
        item_id=command_id,
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.anyio
async def test_command_metric_removal_of_invalid_command(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for(
        "remove_command_usage_metric",
        item_id="f47ac10b-58cc-4372-a567-0e02b2c3d479",
    )
    response = await client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
