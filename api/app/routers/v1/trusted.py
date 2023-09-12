from fastapi import APIRouter

from app.database.models import Trusted

router = APIRouter()


@router.post("/", response_model=Trusted, status_code=201)
async def create_trusted_user(trusted: Trusted) -> Trusted:
    return await trusted.save()


@router.get("/", response_model=list[Trusted])
async def get_all_trusted_users() -> list[Trusted]:
    return await Trusted.objects.all()


@router.get("/{uid}", response_model=Trusted)
async def user_is_trusted(uid: int) -> Trusted:
    is_trusted = await Trusted.objects.get(pk=uid)

    return {"is_trusted": is_trusted}


@router.delete("/{uid}", response_model=Trusted)
async def remove_user_trust(uid: int) -> Trusted:
    item_db = await Trusted.objects.get(pk=uid)

    return {"deleted_rows": await item_db.delete()}
