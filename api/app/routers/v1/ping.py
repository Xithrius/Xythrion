from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def ping() -> dict[str, str]:
    return {"ping": "some amount of time"}
