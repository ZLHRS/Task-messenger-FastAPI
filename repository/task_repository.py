from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from repository.base_repository import BaseRepository
from models.task_model import Task


class TaskRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Task)

    async def get_my_tasks(self, user_id):
        res = await self.db.execute(select(self.model).where(Task.user_id == user_id))
        return res.scalars().all()

    async def get_by_user_id(self, user_id: int, task_id: int):
        result = await self.db.execute(
            select(self.model).where(
                self.model.id == task_id, self.model.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
