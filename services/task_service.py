from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from repository.task_repository import TaskRepository
from repository.user_repository import UserRepository
from schemes.task_schema import CreateTask, PatchTask, TaskUpdateStatus, TaskSchema
from utils.redis_cashe import get_or_set, update_redis


class TaskService:
    def __init__(self, db: AsyncSession):
        self.task_repo = TaskRepository(db)
        self.user_repo = UserRepository(db)

    async def update_redis(self, key):
        data = await self.task_repo.get_all()
        data_dict = [TaskSchema.model_validate(task).model_dump() for task in data]
        await update_redis(key, data_dict)

    async def create_task(self, data: CreateTask):
        new_task = await self.task_repo.create(data)
        return new_task

    async def show_all(self):
        tasks = await self.task_repo.get_all()
        tasks_dict = [TaskSchema.model_validate(task).model_dump() for task in tasks]
        return await get_or_set("tasks:all", 60, tasks_dict)

    async def update_task(self, task_id: int, data: Union[TaskUpdateStatus, PatchTask]):
        model = await self.task_repo.get_by_id(task_id)
        return await self.task_repo.update(model, data.model_dump())

    async def show_my_tasks(self, user_id: int):
        tasks = await self.task_repo.get_my_tasks(user_id)
        tasks_dict = [TaskSchema.model_validate(task).model_dump() for task in tasks]
        return await get_or_set("tasks:my", 60, tasks_dict)

    async def show_task(self, user_id: int, task_id: int):
        return await self.task_repo.get_by_user_id(user_id, task_id)

    async def get_user_by_id(self, user_id):
        return await self.user_repo.get_by_id(user_id)
