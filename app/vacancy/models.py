from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT
from uuid import uuid4, UUID

from app.company.models import Company
from app.competence.models import Competence, CompetenceLevel


class LocationBase(SQLModel):
    country: str = Field(index=True)
    region: str = Field(index=True)
    city: str = Field(index=True)

class Location(LocationBase, table=True):
    __tablename__ = "locations"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    __table_args__ = (
        UniqueConstraint("country", "region", "city", name="uq_location_composite"),
    )
    
    vacancies: list["Vacancy"] = Relationship(back_populates="location", sa_relationship_kwargs={'lazy': 'selectin'})



class VacancyBase(SQLModel):
    name: str = Field(index=True)
    description: str = Field(sa_column=Column(TEXT))
    url: str


class Vacancy(VacancyBase, table=True):
    __tablename__ = "vacancies"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    location_id: UUID = Field(foreign_key="locations.id")
    company_id: UUID = Field(foreign_key="companies.id")


    location: Location = Relationship(back_populates="vacancies", sa_relationship_kwargs={'lazy': 'selectin'})
    company: Company = Relationship(back_populates="vacancies", sa_relationship_kwargs={'lazy': 'selectin'})

    vacancy_competencies: list["VacancyCompetence"] = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})

class VacancyCompetence(CompetenceLevel, table=True):
    __tablename__ = "vacancy_competencies"
    competence_id: str = Field(primary_key=True, foreign_key="competencies.id")
    vacancy_id: UUID = Field(primary_key=True, foreign_key="vacancies.id")

    competence: Competence = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})

    __table_args__ = (
        PrimaryKeyConstraint("vacancy_id", "competence_id", name="vacancy_competence_pk"),
    )



    
    
