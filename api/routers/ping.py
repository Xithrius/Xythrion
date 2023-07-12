from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/")
async def ping() -> dict[str, str]:
    return {"ping": "some amount of time"}
