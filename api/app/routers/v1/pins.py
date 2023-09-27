from fastapi import APIRouter, HTTPException, status
from ormar import NoMatch

from app.database import Pin

router = APIRouter()


@router.post(
    "/",
    response_model=Pin,
    status_code=status.HTTP_201_CREATED,
)
async def create_pin(server_id: int, user_id: int, message: str) -> Pin:
    return await Pin(server_id=server_id, user_id=user_id, message=message).save()


@router.get(
    "/",
    response_model=list[Pin],
    status_code=status.HTTP_200_OK,
)
async def get_all_builds() -> list[Pin]:
    return await Pin.objects.all()


@router.delete(
    "/{id}",
    response_model=Pin,
    status_code=status.HTTP_200_OK,
)
async def remove_build(id: int) -> Pin:
    try:
        item = await Pin.objects.get(id=id)

        await Pin.objects.delete(id=id)

        return item

    except NoMatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deep Rock Galactic build with id '{id}' not found.",
        )
