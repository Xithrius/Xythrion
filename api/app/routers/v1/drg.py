from fastapi import APIRouter, HTTPException, status
from ormar import NoMatch

from app.database import DeepRockGalacticBuild

router = APIRouter()


@router.post(
    "/",
    response_model=DeepRockGalacticBuild,
    status_code=status.HTTP_201_CREATED,
)
async def create_build(build: DeepRockGalacticBuild) -> DeepRockGalacticBuild:
    return await build.save()


@router.get(
    "/",
    response_model=list[DeepRockGalacticBuild],
    status_code=status.HTTP_200_OK,
)
async def get_all_builds() -> list[DeepRockGalacticBuild]:
    return await DeepRockGalacticBuild.objects.all()


@router.delete(
    "/{id}",
    response_model=DeepRockGalacticBuild,
    status_code=status.HTTP_200_OK,
)
async def remove_build(id: int) -> DeepRockGalacticBuild:
    try:
        item = await DeepRockGalacticBuild.objects.get(id=id)

        await DeepRockGalacticBuild.objects.delete(id=id)

        return item

    except NoMatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deep Rock Galactic build with id '{id}' not found.",
        )
