from sqlalchemy.ext.asyncio import AsyncSession
from repository.user_repository import UserRepository
from schemes.user_schema import UserUpdateRole, CreateUser, UserSchema
from utils.redis_cashe import get_or_set, update_redis


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def update_redis(self, key):
        data = await self.user_repo.get_all()
        data_dict = [UserSchema.model_validate(user).model_dump() for user in data]
        return await update_redis(key, data_dict)

    async def show_all(self):
        users = await self.user_repo.get_all()
        user_dict = [UserSchema.model_validate(user).model_dump() for user in users]
        return await get_or_set("users:all", 300, user_dict)

    async def get_user_by_username(self, username: str):
        return await self.user_repo.get_user_by_username(username)

    async def register_user(self, user_data: CreateUser):
        return await self.user_repo.create_obj(user_data)

    async def get_by_id(self, user_id: int):
        return await self.user_repo.get_by_id(user_id)
