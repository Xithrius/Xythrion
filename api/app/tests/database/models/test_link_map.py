import pytest
from app.database.models.link_map import LinkMapChannelModel, LinkMapConverterModel
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.anyio
async def test_create_one_link_map_channel_model(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    data = {
        "server_id": 1111,
        "input_channel_id": 2222,
        "output_channel_id": 3333,
    }
    create_data = LinkMapChannelModel(**data)

    dbsession.add(create_data)
    await dbsession.commit()


@pytest.mark.anyio
async def test_create_one_link_map_converter_model_with_to_link(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    data = {
        "from_link": "example_from_link",
        "to_link": "example_to_link",
    }

    create_data = LinkMapConverterModel(**data)

    dbsession.add(create_data)
    await dbsession.commit()

    created_instance = await dbsession.execute(
        select(LinkMapConverterModel).where(LinkMapConverterModel.id == create_data.id),
    )
    fetched_converter = created_instance.scalar()

    assert fetched_converter is not None
    assert fetched_converter.from_link == data["from_link"]
    assert fetched_converter.to_link == data["to_link"]
    assert fetched_converter.xpath is None


@pytest.mark.anyio
async def test_create_one_link_map_to_link_and_xpath_throws_error(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    data = {
        "from_link": "example_from_link",
        "to_link": "example_to_link",
        "xpath": "some/xpath",
    }
    create_data = LinkMapConverterModel(**data)
    dbsession.add(create_data)

    with pytest.raises(IntegrityError):
        await dbsession.commit()


@pytest.mark.anyio
async def test_create_one_link_map_no_channel_throws_error(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None: ...
