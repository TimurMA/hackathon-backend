from app.skill.models import *

from fastapi_filter.contrib.sqlalchemy import Filter


class SkillSave(SkillBase):
    def to_entity(self):
        return Skill(
            name = self.name,
            skill_type = self.skill_type
        )


class SkillPublic(SkillBase):
    id: str
    @staticmethod
    def init_scheme(skill: Skill):
        skill_id = skill.id.hex
        name = skill.name,
        skill_type = skill.skill_type
        return SkillPublic(
            id=skill_id,
            name = name,
            skill_type = skill_type
        )


class UserSkillPublic(SQLModel):
    user_id: str
    skill_id: str
    skill: SkillPublic
    @staticmethod
    def init_scheme(user_skill: UserSkill):
        return UserSkillPublic(
            user_id=str(user_skill.user_id),
            skill_id=str(user_skill.skill_id),
            skill=SkillPublic.init_scheme(user_skill.skill)
        )


class SkillFilter(Filter):
    id: str | None = None
    name: str | None = None
    skill_type: str | None = None
    class Constants(Filter.Constants):
        model = Skill
