from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter

from app.company.models import CompanyBase, Company, CompanyVacancy
from app.vacancy.schemas import VacancyPublic

from uuid import UUID
from typing import Optional

from app.vacancy.schemas import VacancyFilter


class CompanyPublic(CompanyBase):
    id: str
    name: str
    hr_id: Optional[UUID] = None
    vacancies: list[VacancyPublic]
    @staticmethod
    def init_scheme(company: Company):
        return CompanyPublic(
            id=company.id.hex,
            name=company.name,
            hr_id=company.hr_id,
            vacancies=list(map(VacancyPublic.init_scheme, company.company_vacancy))
        )

class CompanySave(CompanyBase):
    hr_id: Optional[UUID] = None
    def to_entity(self):
        return Company(
            name=self.name,
            hr_id=self.hr_id
        )


class CompanyFilter(Filter):
    id: str | None = None
    name: str | None = None
    hr_id: str | None = None
    vacancies: VacancyFilter | None = FilterDepends(with_prefix("vacancies", VacancyFilter))
    class Constants(Filter.Constants):
        model = Company
