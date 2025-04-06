from sqlalchemy import PrimaryKeyConstraint
from typing import Optional
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field, Relationship

from app.competence.models import Competence, CompetenceLevel


class UserBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True, sa_column_kwargs={"unique": True})
    phone: Optional[str] = Field(default=None, index=True)


class User(UserBase, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    competencies: list["UserCompetence"] = Relationship(back_populates="user",sa_relationship_kwargs={'lazy': 'selectin'})
    is_deleted: bool = Field(default=False, index=True)

class UserCompetence(CompetenceLevel, table=True):
    __tablename__ = "user_competencies"
    competence_id: str = Field(foreign_key="competencies.id")
    user_id: UUID = Field(foreign_key="users.id")

    competence: Competence = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})
    user: User = Relationship(back_populates="competencies", sa_relationship_kwargs={'lazy': 'noload'})

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "competence_id", name="user_competence_pk"),
    )


