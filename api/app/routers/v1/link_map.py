from fastapi import APIRouter, HTTPException, status
from ormar import NoMatch

from app.database import LinkMap

router = APIRouter()


@router.post(
    "/",
    response_model=LinkMap,
    status_code=status.HTTP_201_CREATED,
)
async def create_link_map(link_map: LinkMap) -> LinkMap:
    return await link_map.save()


@router.get(
    "/",
    response_model=list[LinkMap],
    status_code=status.HTTP_200_OK,
)
async def get_link_maps(server_id: int, user_id: int) -> list[LinkMap]:
    return await LinkMap.objects.all(server_id=server_id, user_id=user_id)


@router.delete(
    "/{id}",
    response_model=LinkMap,
    status_code=status.HTTP_200_OK,
)
async def remove_link_map(id: int) -> LinkMap:
    try:
        item = await LinkMap.objects.get(id=id)

        await LinkMap.objects.delete(id=id)

        return item

    except NoMatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Web map with id '{id}' not found.",
        )
