import logging

from app.skill.schemas import *

from sqlalchemy import *
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def get_skill_by_id(skill_id: str, session: AsyncSession) -> SkillPublic:
    result = await session.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="По результатам запроса ничего не было найдено.")
    return SkillPublic.init_scheme(skill)


async def get_all_skills(session: AsyncSession, skill_filter: SkillFilter) -> Sequence[SkillPublic]:
    try:
        query = skill_filter.filter(select(Skill))
        result = await session.execute(query)
        skills = result.scalars().all()
        return [SkillPublic.init_scheme(skill) for skill in skills]
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при получении компетенций.")


async def add_skill(skill_to_save: SkillSave, session: AsyncSession) -> SkillPublic:
    try:
        existing_skill = await session.execute(select(Skill).where(
            Skill.name == skill_to_save.name or
            Skill.skill_type == skill_to_save.skill_type))
        if existing_skill.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Такая компетенция уже существует.")
        skill = skill_to_save.to_entity()
        session.add(skill)
        await session.commit()
        await session.refresh(skill)
        return SkillPublic.init_scheme(skill)
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при добавлении компетенции.")


async def update_skill(skill_id: str, skill_to_update: SkillSave, session: AsyncSession) -> SkillPublic:
    try:
        result = await session.execute(select(Skill).where(Skill.id == skill_id))
        skill = result.scalar_one_or_none()
        if skill is None:
            raise HTTPException(status_code=404, detail="По результатам запроса ничего не было найдено.")
        if (skill.name != skill_to_update.name or
                skill.skill_type != skill_to_update.skill_type):
            existing_skill = await session.execute(select(Skill).where(
                    Skill.name == skill_to_update.name and
                    Skill.skill_type == skill_to_update.skill_type and
                    Skill.id != skill_id))
            if existing_skill.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="Такая компетенция уже существует.")
        skill.name = skill_to_update.name
        skill.skill_type = skill_to_update.skill_type
        session.add(skill)
        await session.commit()
        await session.refresh(skill)
        return SkillPublic.init_scheme(skill)
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при обновлении компетенции.")


async def delete_skill(skill_id: str, session: AsyncSession):
    try:
        result = await session.execute(select(Skill).where(Skill.id == skill_id))
        skill = result.scalar_one_or_none()
        if skill is None:
            raise HTTPException(status_code=404, detail="По результатам запроса ничего не было найдено.")
        await session.delete(skill)
        await session.commit()
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при удалении компетенции.")
