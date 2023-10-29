from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db_session
from app.database.models.deep_rock_galactic import DeepRockGalacticBuildModel

from .schemas import DeepRockGalacticBuild, DeepRockGalacticBuildCreate

router = APIRouter()


@router.post(
    "/",
    response_model=DeepRockGalacticBuild,
    status_code=status.HTTP_201_CREATED,
)
async def create_build(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    build: DeepRockGalacticBuildCreate,
) -> DeepRockGalacticBuildModel:
    new_item = DeepRockGalacticBuildModel(**build.model_dump())

    session.add(new_item)
    await session.flush()

    return new_item


@router.get(
    "/",
    response_model=list[DeepRockGalacticBuild],
    status_code=status.HTTP_200_OK,
)
async def get_all_builds(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int | None = 10,
    offset: int | None = 0,
) -> list[DeepRockGalacticBuildModel]:
    stmt = select(DeepRockGalacticBuildModel).limit(limit).offset(offset)

    items = await session.execute(stmt)

    return list(items.scalars().fetchall())


@router.delete(
    "/{id}",
    response_model=DeepRockGalacticBuild,
    status_code=status.HTTP_200_OK,
)
async def remove_build(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: int,
) -> DeepRockGalacticBuildModel:
    stmt = delete(DeepRockGalacticBuildModel).where(DeepRockGalacticBuildModel.id == id).returning()

    items = await session.execute(stmt)

    return items
