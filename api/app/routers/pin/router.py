from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db_session
from app.database.models.pin import PinModel

from .schemas import Pin, PinCreate

router = APIRouter()


@router.get(
    "/",
    response_model=list[Pin],
    status_code=status.HTTP_200_OK,
)
async def get_all_pins(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: int | None = 10,
    offset: int | None = 0,
) -> list[PinModel]:
    stmt = select(PinModel).limit(limit).offset(offset)

    items = await session.execute(stmt)

    return list(items.scalars().fetchall())


@router.post(
    "/",
    response_model=Pin,
    status_code=status.HTTP_201_CREATED,
)
async def create_pin(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    pin: PinCreate,
) -> PinModel:
    stmt = select(PinModel).where(
        PinModel.server_id == pin.server_id,
        PinModel.channel_id == pin.channel_id,
        PinModel.message_id == pin.message_id,
    )

    items = await session.execute(stmt)

    if items.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pin already exists",
        )

    new_item = PinModel(**pin.model_dump())

    session.add(new_item)
    await session.commit()

    return new_item


@router.delete(
    "/{id}",
    response_model=Pin,
    status_code=status.HTTP_200_OK,
)
async def remove_pin(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: int,
) -> PinModel:
    stmt = delete(PinModel).where(PinModel.id == id).returning()

    items = await session.execute(stmt)

    return items
