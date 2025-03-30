from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field


class CompetenceBase(SQLModel):
    name: str = Field(index=True, unique=True)


class Competence(CompetenceBase, table=True):
    __tablename__ = "competencies"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
