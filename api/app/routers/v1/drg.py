from fastapi import APIRouter

from app.database.models import DeepRockGalacticBuild

router = APIRouter()


@router.post("/", response_model=DeepRockGalacticBuild)
async def create_build(build: DeepRockGalacticBuild) -> DeepRockGalacticBuild:
    return await build.save()


@router.get("/", response_model=list[DeepRockGalacticBuild])
async def get_all_builds() -> list[DeepRockGalacticBuild]:
    return await DeepRockGalacticBuild.objects.all()


@router.delete("/{id}", response_model=DeepRockGalacticBuild)
async def remove_build(id: int) -> DeepRockGalacticBuild:
    item_db = await DeepRockGalacticBuild.objects.get(pk=id)

    return {"deleted_rows": await item_db.delete()}
