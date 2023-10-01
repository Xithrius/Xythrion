from fastapi import APIRouter, HTTPException, status
from ormar import NoMatch

from app.database import Pin

router = APIRouter()


@router.get(
    "/",
    response_model=list[Pin],
    status_code=status.HTTP_200_OK,
)
async def get_all_pins() -> list[Pin]:
    return await Pin.objects.all()


@router.post(
    "/",
    response_model=Pin,
    status_code=status.HTTP_201_CREATED,
)
async def create_pin(pin: Pin) -> Pin:
    if Pin.pk(message=pin.message) is not None:
        return await pin.save()

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Pin already exists",
    )


@router.delete(
    "/{id}",
    response_model=Pin,
    status_code=status.HTTP_200_OK,
)
async def remove_pin(id: int) -> Pin:
    try:
        item = await Pin.objects.get(id=id)

        await Pin.objects.delete(id=id)

        return item

    except NoMatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deep Rock Galactic build with id '{id}' not found.",
        )
