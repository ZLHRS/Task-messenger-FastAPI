from typing import Union
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from schemes.task_schema import CreateTask, PatchTask, TaskUpdateStatus
from services.task_service import TaskService
from utils.celery_app import send_email_async


class TaskUseCase:
    def __init__(self, db: AsyncSession):
        self.task_service = TaskService(db)
        self.db = db

    async def create_task(self, data: CreateTask):
        result = await self.task_service.create_task(data)
        await self.task_service.update_redis("tasks:all")
        data_dict = data.model_dump()
        user_id = data_dict.get("user_id")
        user_data = await self.task_service.get_by_id(user_id)
        send_email_async.delay(user_data.email, "New Task", "Please complete your task")
        return result

    async def show_all(self):
        return await self.task_service.get_all()

    async def update_task(self, task_id: int, data: Union[TaskUpdateStatus, PatchTask]):
        task = await self.task_service.get_by_id(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        dict_task = data.model_dump(exclude_unset=True)
        for key, value in dict_task.items():
            setattr(task, key, value)
        await self.db.commit()
        await self.db.refresh(task)
        await self.task_service.update_redis("tasks:all")
        return task

    async def update_my_task(
        self,
        task_id: int,
        data: Union[TaskUpdateStatus, PatchTask],
        current_user: dict,
    ):
        user_id = current_user.get("user_id")
        task = await self.task_service.get_my_task(user_id, task_id)
        if task is None:
            raise HTTPException(
                status_code=404, detail=["This is not your task or it does not exist"]
            )
        task.status = data.status
        await self.db.commit()
        await self.db.refresh(task)
        await self.task_service.update_redis("tasks:all")
        return task

    async def show_my_tasks(self, current_user: dict):
        user_id = current_user.get("user_id")
        return await self.task_service.get_my_tasks(user_id)
