from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from interfaces.repo_interface import UserRepoInterface
from models.user_model import User
from repository.base_repository import BaseRepository
from schemes.user_schema import CreateUser


class UserRepository(BaseRepository[User, CreateUser], UserRepoInterface[User, CreateUser]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalars().first()
