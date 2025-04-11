from app.user.models import User

from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


class CompanyBase(SQLModel):
    name: str = Field(index=True)


class Company(CompanyBase, table=True):
    __tablename__ = "companies"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hr_id: Optional[UUID] = Field(foreign_key="users.id", default=None)
    HR: Optional[User] = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})
    vacancies: list["Vacancy"] = Relationship(back_populates="company", sa_relationship_kwargs={'lazy': 'selectin'})
