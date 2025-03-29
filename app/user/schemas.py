from app.user.models import *
from app.skill.schemas import *

from fastapi_filter import *
from fastapi_filter.contrib.sqlalchemy import Filter


class UserSave(UserBase):
    skills: list[UUID]
    def to_entity(self):
        return User(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone
        )


class UserPublic(UserBase):
    id: str
    skills: list[SkillPublic]
    @staticmethod
    def init_scheme(user: User):
        return UserPublic(
            id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            is_deleted=user.is_deleted,
            skills=[SkillPublic.init_scheme(user_skill.skill) for user_skill in user.skills]
        )


class UserFilter(Filter):
    id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    is_deleted: bool | None = None
    skills: SkillFilter | None = FilterDepends(with_prefix("skills", SkillFilter))
    class Constants(Filter.Constants):
        model = User
