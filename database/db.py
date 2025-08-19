from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from core.config import data_base

engine = create_async_engine(data_base)
session_local = async_sessionmaker(
    bind=engine, expire_on_commit=True, class_=AsyncSession
)


async def get_session():
    async with session_local() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass
