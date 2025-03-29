from app.skill.models import *

from typing import Optional
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True, sa_column_kwargs={"unique": True})
    phone: Optional[str] = Field(default=None, index=True)


class User(UserBase, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    skills: list["UserSkill"] = Relationship(back_populates="user")
    is_deleted: bool = Field(default=False, index=True)
