from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Column
from sqlalchemy.dialects.postgresql import TEXT
from uuid import uuid4, UUID


class LocationBase(SQLModel):
    country: str = Field(index=True)
    region: str = Field(index=True)
    city: str = Field(index=True)

class Location(LocationBase, table=True):
    __tablename__ = "locations"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    __table_args__ = (
        UniqueConstraint("country", "region", "city", name="uq_location_composite"),
    )
    
    vacancies: list["Vacancy"] = Relationship(back_populates="location", sa_relationship_kwargs={'lazy': 'selectin'})



class VacancyBase(SQLModel):
    name: str = Field(index=True)
    description: str = Field(sa_column=Column(TEXT))
    url: str


class Vacancy(VacancyBase, table=True):
    __tablename__ = "vacancies"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    location_id: UUID = Field(foreign_key="locations.id")


    location: Location = Relationship(back_populates="vacancies", sa_relationship_kwargs={'lazy': 'selectin'})
    


    
    
