from fastapi import APIRouter

from api.database.models import LinkMap

router = APIRouter(prefix="/link_map", tags=["link_map"])


@router.post("/", response_model=LinkMap)
async def create_link_map(link_map: LinkMap) -> LinkMap:
    return await link_map.save()


@router.get("/", response_model=list[LinkMap])
async def get_user_specific_link_maps(sid: int, uid: int) -> list[LinkMap]:
    return await LinkMap.objects.all(sid=sid, uid=uid)
