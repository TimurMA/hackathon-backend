from decimal import Decimal

from sqlmodel import SQLModel

from app.user.models import UserBase, UserCompetence, User
from app.competence.schemas import CompetenceFilter
from app.competence.models import CompetenceBase, CompetenceLevel

from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter

class UserCompetencePublic(CompetenceBase, CompetenceLevel):
    competence_id: str
    user_id: str

    @staticmethod
    def init_scheme(user_competence: UserCompetence):
        return UserCompetencePublic(
            competence_id = user_competence.competence_id,
            level = user_competence.level,
            name = user_competence.competence.name,
            user_id = user_competence.user_id.hex
        )

class UserCompetenceSave(SQLModel):
    competence_id: str
    user_id: str
    level: float

    def to_entity(self):
        return UserCompetence(
            level = Decimal(f"{self.level}"),
            competence_id = self.competence_id,
            user_id = self.user_id
        )


class UserPublic(UserBase):
    id: str
    competencies: list[UserCompetencePublic]
    @staticmethod
    def init_scheme(user: User):
        return UserPublic(
            id = user.id.hex,
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
            phone = user.phone,
            is_deleted = user.is_deleted,
            competencies = list(map(UserCompetencePublic.init_scheme, user.user_competencies))
        )

class UserSave(UserBase):
    competencies: list[UserCompetenceSave]
    def to_entity(self):
        return User(
            first_name = self.first_name,
            last_name = self.last_name,
            email = self.email,
            phone = self.phone
        )

class UserFilter(Filter):
    id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    is_deleted: bool | None = None
    skills: CompetenceFilter | None = FilterDepends(with_prefix("competencies", CompetenceFilter))
    class Constants(Filter.Constants):
        model = User
