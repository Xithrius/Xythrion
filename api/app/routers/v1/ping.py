from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    "/",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
def ping() -> dict[str, str]:
    return {"ping": "some amount of time"}
