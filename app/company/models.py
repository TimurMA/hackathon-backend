from app.user.models import User

from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Index
from sqlmodel import SQLModel, Field, Relationship


class CompanyBase(SQLModel):
    name: str = Field(index=True)


class Company(CompanyBase, table=True):
    __tablename__ = "companies"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hr_id: Optional[UUID] = Field(foreign_key="users.id")
    HR: Optional[User] = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})
    vacancies: list["CompanyVacancy"] = Relationship(back_populates="company", sa_relationship_kwargs={'lazy': 'selectin'})


class CompanyVacancyBase(SQLModel):
    company: UUID = Field(foreign_key="company.id")
    vacancy: UUID = Field(foreign_key="vacancy.id")


class CompanyVacancy(CompanyVacancyBase, table=True):
    __tablename__ = "company_vacancies"
    company_id: UUID = Field(primary_key=True, foreign_key="company.id")
    vacancy_id: UUID = Field(primary_key=True, foreign_key="vacancies.id")
    company: Company = Relationship(back_populates="company_vacancies", sa_relationship_kwargs={'lazy': 'noload'})
    user: User = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})
    __table_args__ = (
        Index("id_company_vacancy", "company_id", "vacancy_id", unique=True),
    )
