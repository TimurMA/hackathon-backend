from decimal import Decimal

from sqlalchemy import Index, Column, DECIMAL
from typing import Optional
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field, Relationship

from app.competence.models import Competence

class UserCompetenceBase(SQLModel):
    level: Decimal = Field(ge=0, le=10, sa_column=Column(DECIMAL(5, 3)))

class UserCompetence(UserCompetenceBase, table=True):
    __tablename__ = "user_competencies"
    competence_id: UUID = Field(primary_key=True, foreign_key="competencies.id")
    user_id: UUID = Field(primary_key=True, foreign_key="users.id")

    competence: Competence = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})

    __table_args__ = (
        Index("id_user_competence", "user_id", "competence_id", unique=True),
    )

class UserBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True, sa_column_kwargs={"unique": True})
    phone: Optional[str] = Field(default=None, index=True)


class User(UserBase, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    competencies: list[UserCompetence] = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})
    is_deleted: bool = Field(default=False, index=True)


