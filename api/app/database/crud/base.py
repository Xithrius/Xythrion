from collections.abc import Callable
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def get_(
        self,
        db: AsyncSession,
        *,
        pk: str | int | UUID | None = None,
    ) -> ModelType | None:
        result = await db.execute(
            select(self.model).where(self.model.id == pk),
        )

        return result.scalars().first()

    # async def get_by_(self, db: AsyncSession, **kwargs) -> ModelType | None:
    #     result = await db.execute(
    #         select(self.model).where(and_(*kwargs))
    #     )

    async def create_(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        create_data = self.model(**obj_in.model_dump())

        db.add(create_data)

        await db.commit()
        await db.refresh(create_data)

        return create_data

    async def delete_(
        self,
        db: AsyncSession,
        *,
        pk: list[int] | list[UUID] | list[str] | Callable,
    ) -> int:
        result = await db.execute(
            delete(self.model).where(
                self.model.id.in_(pk) if isinstance(pk, list) else pk(),
            ),
        )

        return result.rowcount

    # async def update_(
    #     self,
    #     db: AsyncSession,
    #     pk: int,
    #     obj_in: UpdateSchemaType | dict[str, Any],
    #     user_id: int | None = None,
    # ) -> int:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.model_dump(exclude_unset=True)
    #     if user_id:
    #         update_data.update({"update_user": user_id})
    #     result = await db.execute(update(self.model).where(self.model.id == pk).values(**update_data))
    #     return result.rowcount
