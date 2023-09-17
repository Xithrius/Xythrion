from fastapi import APIRouter, HTTPException, status
from ormar import NoMatch

from app.database import WebMap

router = APIRouter()


@router.post(
    "/",
    response_model=WebMap,
    status_code=status.HTTP_201_CREATED,
)
async def create_web_map(web_map: WebMap) -> WebMap:
    return await web_map.save()


@router.get(
    "/",
    response_model=list[WebMap],
    status_code=status.HTTP_200_OK,
)
async def get_web_maps(server_id: int, user_id: int) -> list[WebMap]:
    return await WebMap.objects.all(
        server_id=server_id,
        user_id=user_id,
    )


@router.delete(
    "/{id}",
    response_model=WebMap,
    status_code=status.HTTP_200_OK,
)
async def remove_web_map(id: int) -> WebMap:
    try:
        item = await WebMap.objects.get(id=id)

        await WebMap.objects.delete(id=id)

        return item

    except NoMatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Web map with id '{id}' not found.",
        )
