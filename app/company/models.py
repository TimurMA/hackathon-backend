from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

import app.vacancy.models as vacancy
from app.user.models import User


class CompanyBase(SQLModel):
    name: str = Field(index=True)

class Company(CompanyBase, table=True):
    __tablename__ = "companies"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hr_id: Optional[UUID] = Field(foreign_key="users.id")

    HR: Optional[User] = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})
    vacancies: list["vacancy.Vacancy"] = Relationship(back_populates="company", sa_relationship_kwargs={'lazy': 'selectin'})