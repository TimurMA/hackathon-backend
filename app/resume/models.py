from sqlalchemy import Column, ARRAY, String, PrimaryKeyConstraint
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

from app.competence.models import CompetenceLevel, Competence
from app.vacancy.models import Vacancy


class ResumeBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)

    emails: list[str] = Field(default=[], sa_column=Column(ARRAY(String)))
    urls: list[str] = Field(default=[], sa_column=Column(ARRAY(String)))
    phones: list[str] = Field(default=[], sa_column=Column(ARRAY(String)))

class Resume(ResumeBase, table=True):
    __tablename__ = "resumes"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    vacancy_id: UUID | None = Field(foreign_key='vacancies.id', nullable=True, default=None)

    vacancy: Vacancy | None = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    resume_competencies: list["ResumeCompetence"] = Relationship(back_populates="resume" ,sa_relationship_kwargs={'lazy': 'selectin'})

class ResumeCompetence(CompetenceLevel, table=True):
    __tablename__ = "resume_competence"

    resume_id: UUID = Field(foreign_key='resumes.id')
    competence_id: str = Field(foreign_key='competencies.id')

    competence: Competence = Relationship(sa_relationship_kwargs={'lazy': 'joined'})
    resume: Resume = Relationship(back_populates="resume_competencies", sa_relationship_kwargs={'lazy': 'noload'})

    __table_args__ = (
        PrimaryKeyConstraint("resume_id", "competence_id", name="resume_competence_pk"),
    )
