from app.competence.models import CompetenceBase, Competence

from fastapi_filter.contrib.sqlalchemy import Filter


class CompetenceSave(CompetenceBase):
    def to_entity(self):
        return Competence(
            name = self.name
        )


class CompetencePublic(CompetenceBase):
    id: str
    @staticmethod
    def init_scheme(competence: Competence):
        competence_id = competence.id
        name = competence.name,
        return CompetencePublic(
            id=competence_id,
            name=name
        )

class CompetenceFilter(Filter):
    id: str | None = None
    name: str | None = None
    class Constants(Filter.Constants):
        model = Competence
