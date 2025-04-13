from decimal import Decimal

from sqlalchemy import Column, DECIMAL
from sqlmodel import SQLModel, Field


class CompetenceBase(SQLModel):
    name: str = Field(index=True, unique=True)
    id: str = Field(index=True, primary_key=True)



class Competence(CompetenceBase, table=True):
    __tablename__ = "competencies"


class CompetenceLevel(SQLModel):
    level: Decimal = Field(ge=0, le=10, max_digits=5, decimal_places=3)