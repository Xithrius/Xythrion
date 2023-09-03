from fastapi import APIRouter

from app.database.models import WebPath

router = APIRouter()


@router.post("/", response_model=WebPath)
async def create_web_map(web_map: WebPath) -> WebPath:
    return await web_map.save()


@router.get("/", response_model=list[WebPath])
async def get_web_maps(sid: int, uid: int) -> list[WebPath]:
    return await WebPath.objects.all(sid=sid, uid=uid)


@router.delete("/{id}", response_model=WebPath)
async def remove_web_map(id: int) -> WebPath:
    item_db = await WebPath.objects.get(pk=id)

    return {"deleted_rows": await item_db.delete()}
