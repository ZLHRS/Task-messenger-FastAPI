from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import UserService
from schemes.user_schema import CreateUser, UserUpdateRole
from utils.security import hash_password


class UserUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_service = UserService(db)

    async def show_all(self):
        return await self.user_service.show_all()

    async def create_user(self, user_data: CreateUser):
        existing_user = await self.user_service.get_user_by_username(user_data.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        user_data = user_data.model_copy(
            update={"password": hash_password(user_data.password)}
        )
        await self.user_service.update_redis("users:all")
        user_dict = user_data.model_dump()
        if (
            not user_dict["email"].endswith("@gmail.com")
            and len(user_dict["email"]) > 10
        ):
            raise HTTPException(status_code=404, detail=["Please write gmail"])
        return await self.user_service.register_user(user_data)

    async def upgrade_downgrade(self, user_id: int, update_role: UserUpdateRole):
        user = await self.user_service.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User is not found")
        if update_role:
            user.role = update_role.role
        await self.db.commit()
        await self.db.refresh(user)
        await self.user_service.update_redis("users:all")
        return user
