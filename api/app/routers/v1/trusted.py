from asyncpg import UniqueViolationError
from fastapi import APIRouter, HTTPException, status
from ormar import NoMatch

from app.database import Trusted

router = APIRouter()


@router.get(
    "/",
    response_model=list[Trusted],
    status_code=status.HTTP_200_OK,
)
async def get_all_trusted_users() -> list[Trusted]:
    return await Trusted.objects.all()


@router.get(
    "/{user_id}",
    response_model=Trusted,
    status_code=status.HTTP_200_OK,
)
async def get_trusted_user(user_id: int) -> Trusted:
    try:
        return await Trusted.objects.get(user_id=user_id)
    except NoMatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trusted user with id '{user_id}' not found.",
        )


@router.post(
    "/",
    response_model=Trusted,
    status_code=status.HTTP_201_CREATED,
)
async def create_trusted_user(trusted: Trusted) -> Trusted:
    try:
        return await trusted.save()
    except UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Trusted user with id '{trusted.id}' already exists.",
        )


@router.delete(
    "/{user_id}",
    response_model=Trusted,
    status_code=status.HTTP_200_OK,
)
async def remove_trusted_user(user_id: int) -> Trusted:
    try:
        item = await Trusted.objects.get(user_id=user_id)

        await Trusted.objects.delete(user_id=user_id)

        return item
    except NoMatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trusted user with id '{user_id}' not found.",
        )
