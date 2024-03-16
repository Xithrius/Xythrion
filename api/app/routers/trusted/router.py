from app.database.dependencies import DBSession
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import delete, select

from app.database.models.trusted import TrustedModel

from .schemas import Trusted, TrustedCreate

router = APIRouter()


@router.get(
    "/",
    response_model=list[Trusted],
    status_code=status.HTTP_200_OK,
)
async def get_all_trusted_users(
    session: DBSession,
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
    session: DBSession,
    user_id: int,
) -> TrustedModel:
    stmt = select(TrustedModel).where(TrustedModel.user_id == user_id)

    items = await session.execute(stmt)
    items.unique()

    if (item := items.scalar_one_or_none()) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trusted user with ID '{user_id}' not found",
        )

    return item


@router.post(
    "/",
    response_model=Trusted,
    status_code=status.HTTP_201_CREATED,
)
async def create_trusted_user(
    session: DBSession,
    trusted: TrustedCreate,
) -> TrustedModel:
    stmt = select(TrustedModel).where(TrustedModel.user_id == trusted.user_id)

    items = await session.execute(stmt)

    if items.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already trusted",
        )

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
    session: DBSession,
    user_id: int,
) -> TrustedModel:
    stmt = delete(TrustedModel).where(TrustedModel.user_id == user_id).returning()

    items = await session.execute(stmt)

    return items
