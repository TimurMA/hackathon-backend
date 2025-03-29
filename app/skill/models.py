from app.user.models import User
from app.skill import skill_type_enum

from uuid import uuid4, UUID
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship


class SkillBase(SQLModel):
    name: str = Field(index=True)
    skill_type: "skill_type_enum" = Field(index=True, description="Type of the skill")


class Skill(SkillBase, table=True):
    __tablename__ = "skills"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    __table_args__ = (
        UniqueConstraint("name", "skill_type", name="uq_skill_composite"),
    )
    user_skills: list["UserSkill"] = Relationship(back_populates="skill")


class UserSkillLink(SQLModel, table=True):
    skill_id: UUID = Field(foreign_key="skills.id")
    user_id: UUID = Field(foreign_key="users.id")


class UserSkill(UserSkillLink, table=True):
    __tablename__ = "user_skills"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    skill: "Skill" = Relationship(back_populates="user_skills")
    user: "User" = Relationship(back_populates="skills")
