import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health(client: AsyncClient, fastapi_app: FastAPI) -> None:
    url = fastapi_app.url_path_for("health_check")

    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
