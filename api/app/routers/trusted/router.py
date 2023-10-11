from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db_session
from app.database.models.trusted import TrustedModel

from .schemas import Trusted, TrustedCreate

router = APIRouter()


@router.get(
    "/",
    response_model=list[Trusted],
    status_code=status.HTTP_200_OK,
)
async def get_all_trusted_users(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int | None = 10,
    offset: int | None = 0,
) -> list[TrustedModel]:
    stmt = select(TrustedModel).limit(limit).offset(offset)

    items = await session.execute(stmt)

    return list(items.scalars().fetchall())


@router.get(
    "/{user_id}",
    response_model=Trusted,
    status_code=status.HTTP_200_OK,
)
async def get_trusted_user(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user_id: int,
    limit: int | None = 10,
    offset: int | None = 0,
) -> list[TrustedModel]:
    stmt = select(TrustedModel).limit(limit).offset(offset)

    items = await session.execute(stmt)

    return list(items.scalars().fetchall())


@router.post(
    "/",
    response_model=Trusted,
    status_code=status.HTTP_201_CREATED,
)
async def create_trusted_user(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    trusted: TrustedCreate,
) -> TrustedModel:
    new_item = TrustedModel(**trusted.model_dump())

    session.add(new_item)
    await session.flush()

    return new_item


@router.delete(
    "/{user_id}",
    response_model=Trusted,
    status_code=status.HTTP_200_OK,
)
async def remove_trusted_user(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user_id: int,
) -> TrustedModel:
    stmt = delete(TrustedModel).where(TrustedModel.user_id == user_id).returning()

    items = await session.execute(stmt)

    return items
