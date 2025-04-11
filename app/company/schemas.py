from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter

from app.vacancy.models import VacancyBase
from app.company.models import CompanyBase, Company, CompanyVacancy, CompanyVacancyBase

from uuid import UUID
from typing import Optional

from app.vacancy.schemas import VacancyFilter


class CompanyVacancyPublic(CompanyBase, VacancyBase):
    company_id: str
    vacancy_id: str
    @staticmethod
    def init_scheme(company_vacancy: CompanyVacancy):
        return CompanyVacancyBase(
            company_id=company_vacancy.company_id,
            vacancy_id=company_vacancy.vacancy_id
        )

class CompanyVacancySave(CompanyVacancyBase):
    company_id: str
    vacancy_id: str
    def to_entity(self):
        return CompanyVacancy(
            company_id=self.company_id,
            vacancy_id=self.vacancy_id
        )


class CompanyPublic(CompanyBase):
    name: str
    hr_id: Optional[UUID] = None
    @staticmethod
    def init_scheme(company: Company):
        return CompanyPublic(
            id=company.id.hex,
            name=company.name,
            hr_id=company.hr_id,
            vacancies=list(map(CompanyVacancyPublic.init_scheme, company.company_vacancy))
        )

class CompanySave(CompanyBase):
    hr_id: Optional[UUID] = None
    vacancies: list[CompanyVacancySave]
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
