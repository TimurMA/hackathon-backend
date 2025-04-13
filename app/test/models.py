from sqlalchemy import TIMESTAMP
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from uuid import uuid4, UUID
from datetime import datetime, timezone

from app.company.models import Company
from app.user.models import User
from app.vacancy.models import VacancyCompetence


class QuestionType(str, Enum):
    SINGLE = 'single'
    MULTIPLE = 'multiple'
    TEXT = 'text'

class VacancyCompetenceTest(SQLModel, table=True):
    __tablename__ = "vacancy_competence_tests"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    test_id: UUID = Field(foreign_key="tests.id")
    vacancy_id: UUID = Field(foreign_key="vacancies.id")
    competence_id: UUID = Field(foreign_key="competencies.id")

class TestBase(SQLModel):
    name: str = Field(max_length=255)
    test_time: int = Field(default=0)

class Test(TestBase, table=True):
    __tablename__ = "tests"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    company_id = Field(foreign_key="companies.id")

    company: Company = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    vacancy_competencies: list[VacancyCompetence] = Relationship(sa_relationship_kwargs={"lazy": "selectin"}, link_model=VacancyCompetenceTest)

class TestResultBase(SQLModel):
    started_at: datetime = Field(sa_column=TIMESTAMP(True))
    finished_at: datetime = Field(default=datetime.now(timezone.utc), sa_column=TIMESTAMP(True))

class TestResult(TestResultBase, table=True):
    __tablename__ = "test_results"
    id: UUID = Field(foreign_key="tests.id", primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")

    user: User = Relationship(sa_relationship_kwargs={ "lazy": "selectin" })
    user_choices: list["UserChoice"] = Relationship(back_populates="test_result", sa_relationship_kwargs={ "lazy": "selectin"})


class QuestionBase(SQLModel):
    q_type: QuestionType = Field(default=QuestionType.SINGLE)
    question: str = Field(max_length=255)

class AnswerBase(SQLModel):
    answer: str = Field(max_length=255)
    value: int = Field(default=0, ge=-10, le=10)

class UserChoiceBase(SQLModel):
    is_selected: bool = Field(default=False)

class UserChoice(UserChoiceBase, table=True):
    __tablename__ = "user_choices"

    test_result_id: UUID = Field(foreign_key="test_results.id")
    answer_id: UUID = Field(foreign_key="answers.id")

    test_result: TestResult = Relationship(back_populates="user_choices", sa_relationship_kwargs={"lazy": "noload"})

