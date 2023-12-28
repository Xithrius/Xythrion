import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


@pytest.mark.anyio
async def test_creation(
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
