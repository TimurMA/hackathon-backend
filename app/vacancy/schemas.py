from decimal import Decimal
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_filter import FilterDepends, with_prefix
from sqlmodel import SQLModel, Field

from app.company.models import Company
from app.competence.models import CompetenceBase
from app.vacancy.models import Location, LocationBase, VacancyBase, Vacancy, VacancyCompetence, CompetenceLevel

class LocationSave(LocationBase):
    def to_entity(self):
        return Location(
            country = self.country,
            region = self.region,
            city = self.city
        )
        
class LocationPublic(LocationBase):
    id: str
    
    @staticmethod
    def init_scheme(location: Location):
        return LocationPublic(
            id = location.id.hex,
            country = location.country,
            region = location.region,
            city = location.city
        )

class VacancyCompetenceSave(SQLModel):
    competence_id: str
    level: float

    def to_entity(self, vacancy_id):
        return VacancyCompetence(
            vacancy_id = UUID(vacancy_id),
            competence_id = self.competence_id,
            level = Decimal(f"{self.level}")
        )

class VacancyCompetencePublic(CompetenceLevel, CompetenceBase):
    competence_id: str
    vacancy_id: str

    @staticmethod
    def init_scheme(vacancy_competence: VacancyCompetence):
        return VacancyCompetencePublic(
            name = vacancy_competence.competence.name,
            competence_id = vacancy_competence.competence_id,
            vacancy_id = vacancy_competence.vacancy_id.hex,
            level = vacancy_competence.level
        )

class VacancySave(VacancyBase):
    location: LocationSave
    company_id: str
    vacancy_competencies: list[VacancyCompetenceSave] = Field(default=list)
    def to_entity(self):
        return Vacancy(
            name = self.name,
            description = self.description,
            url = self.url,
            company_id = UUID(self.company_id),
        )
    

class VacancyPublic(VacancyBase):
    id: str
    location: LocationPublic
    location_id: str
    company_id: str

    vacancy_competencies: list["VacancyCompetencePublic"]
    
    @staticmethod
    def init_scheme(vacancy: Vacancy):
        return VacancyPublic(
            id = vacancy.id.hex,
            name = vacancy.name,
            description = vacancy.description,
            url = vacancy.url,
            location_id = vacancy.location_id.hex,
            company_id = vacancy.company_id.hex,
            location = LocationPublic.init_scheme(vacancy.location),
            vacancy_competencies = list(map(VacancyCompetencePublic.init_scheme, vacancy.vacancy_competencies))
        )
 
class CompanyFilter(Filter):
    id: str | None = None
    name: str | None = None
    hr_id: str | None = None
    class Constants(Filter.Constants):
        model = Company


class LocationFilter(Filter):
    id: str | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None

    class Constants(Filter.Constants):
        model = Location


class VacancyFilter(Filter):
    id: str | None = None
    location: LocationFilter | None = FilterDepends(with_prefix("location", LocationFilter))
    company: CompanyFilter | None = FilterDepends(with_prefix('company', CompanyFilter))
    class Constants(Filter.Constants):
        model = Vacancy