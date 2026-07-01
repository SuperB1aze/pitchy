from typing import Any, ClassVar

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class BaseServiceORM:
    model: ClassVar[Any] = None
    not_found_detail: ClassVar[str] = "Object not found"

    @classmethod
    def check_model(cls):
        if cls.model is None:
            raise RuntimeError(f"{cls.__name__}.model is not set")

    @classmethod
    def list_query(cls):
        cls.check_model()
        return select(cls.model)

    @classmethod
    def detail_query(cls, object_id: int):
        cls.check_model()
        return select(cls.model).where(cls.model.id == object_id)

    @classmethod
    async def get_or_404(cls, session: AsyncSession, object_id: int):
        obj = await session.get(cls.model, object_id)
        if obj is None:
            raise HTTPException(status_code=404, detail=cls.not_found_detail)
        return obj

    @classmethod
    async def show_all(cls, session: AsyncSession):
        cls.check_model()
        result = await session.execute(cls.list_query())
        return result.scalars().all()

    @classmethod
    async def show_one(cls, session: AsyncSession, object_id: int):
        cls.check_model()
        result = await session.execute(cls.detail_query(object_id))
        obj = result.scalar_one_or_none()
        if obj is None:
            raise HTTPException(status_code=404, detail=cls.not_found_detail)
        return obj

    @classmethod
    async def create(cls, session: AsyncSession, **data: Any):
        cls.check_model()
        obj = cls.model(**data)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def update(cls, session: AsyncSession, object_id: int, **data: Any):
        obj = await cls.get_or_404(session, object_id)
        for key, value in data.items():
            setattr(obj, key, value)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def hard_delete(cls, session: AsyncSession, object_id: int):
        obj = await cls.get_or_404(session, object_id)
        await session.delete(obj)
        await session.commit()
        return {"detail": "Successfully deleted"}