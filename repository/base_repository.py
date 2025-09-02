from typing import Generic, TypeVar, Type, Optional, Iterable
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from interfaces.repo_interface import BaseRepoInterface

T = TypeVar('T')
CreateT = TypeVar('CreateT', bound=BaseModel)

class BaseRepository(BaseRepoInterface[T, CreateT], Generic[T, CreateT]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        result = await self.db.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()

    async def get_all(self) -> Iterable[T]:
        result = await self.db.execute(select(self.model))
        return result.scalars().all()

    async def create_obj(self, obj_data:CreateT) -> T:
        obj = self.model(**obj_data.model_dump())
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete_obj(self, obj:int) -> None:
        result = await self.db.execute(select(self.model).where(self.model.id == obj))
        instance = result.scalars().first()
        if not instance:
            return
        await self.db.delete(instance)
        await self.db.commit()

