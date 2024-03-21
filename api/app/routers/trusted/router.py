from fastapi import APIRouter, HTTPException, Response, status

from app.database.crud.trusted import trusted_dao
from app.database.dependencies import DBSession
from app.database.models.trusted import TrustedModel

from .schemas import Trusted, TrustedCreate

router = APIRouter()


@router.get(
    "/",
    response_model=list[Trusted],
    status_code=status.HTTP_200_OK,
)
async def get_all_trusted_users(
    session: DBSession,
    limit: int | None = 10,
    offset: int | None = 0,
) -> list[TrustedModel]:
    return await trusted_dao.get_all(session, limit=limit, offset=offset)


@router.get(
    "/{user_id}",
    response_model=Trusted,
    status_code=status.HTTP_200_OK,
)
async def get_trusted_user(
    session: DBSession,
    user_id: int,
) -> TrustedModel:
    user = await trusted_dao.get_by_user_id(session, user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trusted user with ID '{user_id}' not found",
        )

    return user


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_trusted_user(
    session: DBSession,
    new_user: TrustedCreate,
) -> None:
    user = await trusted_dao.get_by_user_id(session, user_id=new_user.user_id)

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already trusted",
        )

    await trusted_dao.create(session, obj_in=new_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_trusted_user(
    session: DBSession,
    user_id: int,
) -> None:
    count = await trusted_dao.delete(session, pk=[user_id])

    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trusted user with ID '{user_id}' not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
