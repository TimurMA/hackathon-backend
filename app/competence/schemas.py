from app.competence.models import CompetenceBase, Competence

from fastapi_filter.contrib.sqlalchemy import Filter


class CompetenceSave(CompetenceBase):
    id: str
    def to_entity(self):
        return Competence(
            name=self.name,
            id=self.id
        )


class CompetencePublic(CompetenceBase):
    id: str
    @staticmethod
    def init_scheme(competence: Competence):
        return CompetencePublic(
            id=competence.id,
            name=competence.name
        )

class CompetenceFilter(Filter):
    id: str | None = None
    name: str | None = None
    class Constants(Filter.Constants):
        model = Competence
