from sqlalchemy import TIMESTAMP
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from uuid import uuid4, UUID
from datetime import datetime, timezone

from app.company.models import Company
from app.resume.models import Resume
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
    questions: list["Question"] = Relationship(back_populates="test", sa_relationship_kwargs={"lazy": "selectin"})

class TestResultBase(SQLModel):
    started_at: datetime = Field(default=datetime.now(timezone.utc), sa_column=TIMESTAMP(True))
    finished_at: datetime = Field(sa_column=TIMESTAMP(True))
    max_result: int
    result: int = Field(default=0)

class TestResult(TestResultBase, table=True):
    __tablename__ = "test_results"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    test_id: UUID = Field(foreign_key="tests.id")
    resume_id: UUID = Field(foreign_key="resumes.id")

    resume: Resume = Relationship(sa_relationship_kwargs={ "lazy": "selectin" })
    choices: list["Choice"] = Relationship(back_populates="test_result", sa_relationship_kwargs={ "lazy": "selectin"})
    test: Test = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


class QuestionBase(SQLModel):
    q_type: QuestionType = Field(default=QuestionType.SINGLE)
    question: str = Field(max_length=255)

class Question(QuestionBase, table=True):
    __tablename__ = "questions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    test_id: UUID = Field(foreign_key="tests.id")

    test: Test = Relationship(back_populates="questions", sa_relationship_kwargs={"lazy": "noload"})
    answers: list["Answer"] = Relationship(back_populates="question", sa_relationship_kwargs={"lazy": "selectin"})

class AnswerBase(SQLModel):
    answer: str = Field(max_length=255)
    value: int = Field(default=0, ge=-10, le=10)


class Answer(AnswerBase, table=True):
    __tablename__ = "answers"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    question_id: UUID = Field(foreign_key="questions.id")

    question: Question = Relationship(back_populates="answers", sa_relationship_kwargs={"lazy": "noload"})


class ChoiceBase(SQLModel):
    is_selected: bool = Field(default=False)

class Choice(ChoiceBase, table=True):
    __tablename__ = "user_choices"

    test_result_id: UUID = Field(foreign_key="test_results.id")
    answer_id: UUID = Field(foreign_key="answers.id", primary_key=True)

    test_result: TestResult = Relationship(back_populates="user_choices", sa_relationship_kwargs={"lazy": "noload"})
    answer: Answer = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


