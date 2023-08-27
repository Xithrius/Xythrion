from fastapi import APIRouter

from app.database.models import LinkMap

router = APIRouter()


@router.post("/", response_model=LinkMap)
async def create_link_map(link_map: LinkMap) -> LinkMap:
    return await link_map.save()


@router.get("/", response_model=list[LinkMap])
async def get_link_maps(sid: int, uid: int) -> list[LinkMap]:
    return await LinkMap.objects.all(sid=sid, uid=uid)


@router.delete("/{id}", response_model=LinkMap)
async def remove_link_map(id: int) -> LinkMap:
    item_db = await LinkMap.objects.get(pk=id)

    return {"deleted_rows": await item_db.delete()}
