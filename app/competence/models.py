from decimal import Decimal

from sqlalchemy import Column, DECIMAL, CheckConstraint, UniqueConstraint
from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID


class CompetenceBase(SQLModel):
    name: str = Field(index=True, unique=True)

class Competence(CompetenceBase, table=True):
    id: str = Field(index=True, primary_key=True)
    __tablename__ = "competencies"

class CompetenceLevel(SQLModel):
    level: Decimal = Field(ge=0, le=10, max_digits=5, decimal_places=3)

class CompetenceContiguity(SQLModel, table=True):
    __tablename__ = "competence_contiguities"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    first_competence_id: str = Field(foreign_key="competencies.id")
    second_competence_id: str = Field(foreign_key="competencies.id")
    contiguity_coefficient: Decimal = Field(ge=0, le=1, max_digits=4, decimal_places=3)

    __table_args__ = (
        CheckConstraint("first_competence_id != second_competence_id", name="check_first_not_second"),
        UniqueConstraint("first_competence_id", "second_competence_id", name="uq_group_competence_id")
    )

