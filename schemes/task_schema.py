from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    planned = "planned"
    active = "active"
    blocked = "blocked"
    finished = "finished"


class BaseTask(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=300)
    status: TaskStatus = TaskStatus.planned
    user_id: int


class CreateTask(BaseTask):
    pass


class TaskSchema(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=300)
    status: TaskStatus = TaskStatus.planned
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class PatchTask(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=3, max_length=300)
    status: Optional[TaskStatus] = None
    user_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class TaskUpdateStatus(BaseModel):
    status: TaskStatus
