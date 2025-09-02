from fastapi import APIRouter
from fastapi.params import Depends
from typing import List, Any, Annotated
from core.dependencies import get_current_admin, get_current_user
from schemes.auth_schema import CurrentUser
from schemes.task_schema import CreateTask, TaskSchema, PatchTask, TaskUpdateStatus
from use_cases.task_use_case import TaskUseCase
from database.db import SessionDep

router = APIRouter(prefix="/task")


@router.get(
    "/",
    tags=["Admin Panel"],
    response_model=List[TaskSchema],
    dependencies=[Depends(get_current_admin)],
)
async def show_task(session: SessionDep):
    use_case = TaskUseCase(session)
    return await use_case.show_all()


@router.post(
    "/",
    tags=["Admin Panel"],
    response_model=TaskSchema,
    dependencies=[Depends(get_current_admin)],
)
async def create_task(data: CreateTask, session: SessionDep):
    use_case = TaskUseCase(session)
    return await use_case.create_task(data)


@router.patch(
    "/{task_id}",
    tags=["Admin Panel"],
    response_model=TaskSchema,
    dependencies=[Depends(get_current_admin)],
)
async def update_task(task_id: int, data: PatchTask, session: SessionDep):
    use_case = TaskUseCase(session)
    return await use_case.update_task(task_id, data)


@router.get(
    "/my_tasks",
    tags=["User Panel"],
    response_model=List[TaskSchema],
    dependencies=[Depends(get_current_user)],
)
async def show_my_tasks(
    session: SessionDep, current_user: Annotated[dict[Any, Any], Depends(get_current_user)]
):
    use_case = TaskUseCase(session)
    return await use_case.show_my_tasks(current_user)


@router.patch(
    "/{task_id}/update_status",
    tags=["User Panel"],
    response_model=TaskSchema,
    dependencies=[Depends(get_current_user)],
)
async def update_status(
    task_id: int,
    data: TaskUpdateStatus,
    session: SessionDep,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    use_case = TaskUseCase(session)
    return await use_case.update_my_task(task_id, data, current_user)
