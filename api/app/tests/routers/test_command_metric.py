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

    # response = await client.put(
    #     url,
    #     json={
    #         "name": test_name,
    #     },
    # )
    # assert response.status_code == status.HTTP_200_OK
    # dao = DummyDAO(dbsession)
    # instances = await dao.filter(name=test_name)
    # assert instances[0].name == test_name


# @pytest.mark.anyio
# async def test_getting(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     dbsession: AsyncSession,
# ) -> None:
#     """Tests dummy instance retrieval."""
#     dao = DummyDAO(dbsession)
#     test_name = uuid.uuid4().hex
#     await dao.create_dummy_model(name=test_name)
#     url = fastapi_app.url_path_for("get_dummy_models")
#     response = await client.get(url)
#     dummies = response.json()

#     assert response.status_code == status.HTTP_200_OK
#     assert len(dummies) == 1
#     assert dummies[0]["name"] == test_name
