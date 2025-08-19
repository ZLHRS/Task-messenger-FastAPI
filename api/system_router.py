from fastapi import APIRouter
from starlette.responses import Response
from models.user_model import User
from database.db import engine, Base, session_local, SessionDep
from schemes.user_schema import UserRole
from use_cases.auth_use_cases import AuthUseCases
from utils.security import hash_password
from core.config import admin_info

router = APIRouter(prefix="/System", tags=["System"])


@router.post("/Drop_Create_DataBase")
async def setup_database(response: Response, session_db: SessionDep):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with session_local() as session:
        user = User(
            username=admin_info.ADMIN_USERNAME,
            email="shaykenov.danialg@gmail.com",
            password=hash_password(admin_info.ADMIN_PASSWORD),
            role=UserRole("admin"),
        )
        session.add(user)
        await session.commit()

    use_case = AuthUseCases(session_db)
    await use_case.logout(response)
    return {"message": "success"}
