from fastapi import APIRouter, HTTPException, Response, status

from app.database.crud.pin import pin_dao
from app.database.dependencies import DBSession
from app.database.models.pin import PinModel

from .schemas import Pin, PinBase, PinCreate

router = APIRouter()


@router.get(
    "/",
    response_model=list[Pin],
    status_code=status.HTTP_200_OK,
)
async def get_all_pins(
    session: DBSession,
    limit: int = 10,
    offset: int = 0,
) -> list[PinModel]:
    items = await pin_dao.get_all(session, offset=offset, limit=limit)

    return list(items)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_pin(
    session: DBSession,
    new_pin: PinCreate,
) -> None:
    pins = await pin_dao.get_by_section_ids(session, pin=new_pin)

    if pins is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pin already exists",
        )

    await pin_dao.create(session, obj_in=new_pin)


@router.delete(
    "/{server_id}/{channel_id}/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_pin(
    session: DBSession,
    server_id: int,
    channel_id: int,
    message_id: int,
) -> Response:
    count = await pin_dao.delete(
        session,
        pin=PinBase(
            server_id=server_id,
            channel_id=channel_id,
            message_id=message_id,
        ),
    )

    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pin at {server_id}/{channel_id}/{message_id} not found.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
