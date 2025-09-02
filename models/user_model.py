from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum
from database.db import Base
from enum import Enum as PyEnum
from typing import List

from models.task_model import Task


class UserRole(PyEnum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column("users_id", primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False, default=UserRole.user
    )
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="user")
