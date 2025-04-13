import logging
from typing import Sequence, cast
from fastapi import HTTPException
from sqlalchemy import Select
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.competence.schemas import CompetencePublic, CompetenceFilter, CompetenceSave
from app.competence.models import Competence



async def get_competence_by_id(skill_id: str, session: AsyncSession) -> CompetencePublic:
    query = select(Competence).where(Competence.id == skill_id)
    query = cast(Select[Competence], query)

    result = await session.exec(query)

    competence = result.first()
    if not competence:
        raise HTTPException(status_code=404, detail="По результатам запроса ничего не было найдено.")
    return CompetencePublic.init_scheme(competence)


async def get_all_competence(session: AsyncSession, competence_filter: CompetenceFilter) -> Sequence[CompetencePublic]:
    try:
        query = competence_filter.filter(select(Competence))
        result = await session.exec(query)
        return list(map(CompetencePublic.init_scheme, result.all()))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при получении компетенций.")


async def add_competence(competence_to_save: CompetenceSave, session: AsyncSession) -> CompetencePublic:
    query = select(Competence).where(Competence.name == competence_to_save.name)
    query = cast(Select[Competence], query)
    existing_competence = await session.exec(query)
    if existing_competence.first():
        await session.rollback()
        raise HTTPException(status_code=400, detail="Такая компетенция уже существует.")

    try:
        competence = competence_to_save.to_entity()
        session.add(competence)
        await session.commit()
        await session.refresh(competence)
        return CompetencePublic.init_scheme(competence)
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при добавлении компетенции.")


async def update_competence(competence_id: str,
                            competence_to_update: CompetenceSave,
                            session: AsyncSession) -> CompetencePublic:
    query = select(Competence).where(Competence.id == competence_id)
    query = cast(Select[Competence], query)

    result = await session.exec(query)
    competence = result.first()

    if competence is None:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Компетенция не найдена.")

    if competence.name != competence_to_update.name:
        query = select(Competence).where(Competence.name == competence_to_update.name)
        query = cast(Select[Competence], query)
        existing_competence = await session.exec(query)
        if existing_competence.first():
            await session.rollback()
            raise HTTPException(status_code=400, detail="Такая компетенция уже существует.")

    try:
        competence.name = competence_to_update.name

        session.add(competence)
        await session.commit()
        await session.refresh(competence)

        return CompetencePublic.init_scheme(competence)
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при обновлении компетенции.")


async def delete_competence(competence_id: str, session: AsyncSession):
    query = select(Competence).where(Competence.id == competence_id)
    query = cast(Select[Competence], query)

    result = await session.exec(query)
    competence = result.first()

    if competence is None:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Компетенции не существует")

    try:
        await session.delete(competence)
        await session.commit()
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при удалении компетенции.")
