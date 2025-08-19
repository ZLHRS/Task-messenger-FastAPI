from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class BaseRepository:
    def __init__(self, db: AsyncSession, model):
        self.db = db
        self.model = model

    async def get_by_id(self, obj_id: int):
        result = await self.db.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(self.model))
        return result.scalars().all()

    async def create(self, obj_data):
        obj = self.model(**obj_data.model_dump())
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj):
        await self.db.delete(obj)
        await self.db.commit()
