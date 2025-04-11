from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from uuid import uuid4, UUID

from app.user.models import User


class QuestionType(str, Enum):
    SINGLE = 'single'
    MULTIPLE = 'multiple'

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

    question_id: UUID = Field(foreign_key="questions.id")
    answer_id: UUID = Field(foreign_key="answers.id")
    user_id: UUID = Field(foreign_key="users.id")

    user: User = Relationship(sa_relationship_kwargs={ "lazy": "selectin"})


