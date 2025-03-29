from app.db import Session
from app.skill.service import *
from app.skill.schemas import *

from fastapi import APIRouter
from fastapi_filter import FilterDepends


skill_router = APIRouter(
    prefix="/skill",
    tags=["Skill"]
)


@skill_router.get("/{skill_id}")
async def get_skill_by_id_async(skill_id: str, session: Session) -> SkillPublic:
    return await get_skill_by_id(skill_id, session)


@skill_router.get("/all")
async def get_all_skills_async(session: Session, skill_filter: SkillFilter = FilterDepends(SkillFilter)) -> Sequence[SkillPublic]:
    return await get_all_skills(session, skill_filter)


@skill_router.post("/add")
async def add_skill_async(skill: SkillSave, session: Session) -> SkillPublic:
    return await add_skill(skill, session)


@skill_router.put("/update/{skill_id}")
async def update_skill_async(skill_id: str, skill: SkillSave, session: Session) -> SkillPublic:
    return await update_skill(skill_id, skill, session)


@skill_router.delete("/{skill_id}")
async def delete_skill_async(skill_id: str, session: Session):
    return await delete_skill(skill_id, session)
