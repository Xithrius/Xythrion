from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, status

router = APIRouter()

timezone_offset: float = 0.0
tzinfo = timezone(timedelta(hours=timezone_offset))


@router.get(
    "/",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
def ping() -> dict[str, str]:
    return {"ping": datetime.now(tz=tzinfo).isoformat()}
