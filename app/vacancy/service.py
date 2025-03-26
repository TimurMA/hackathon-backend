from typing import Sequence
from fastapi import HTTPException
import logging
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.vacancy.models import Vacancy, Location
from app.vacancy.schemas import VacancyPublic, VacancyFilter, VacancySave, LocationSave, LocationPublic

async def _get_or_create_location(session: AsyncSession, location_data: LocationSave) -> Location:
        existing = await session.exec(
            select(Location).where(
                Location.country == location_data.country,
                Location.region == location_data.region,
                Location.city == location_data.city
            )
        )
        existing = existing.first()
        
        if existing:
            return existing
        else:
            new_location = location_data.to_entity()
            session.add(new_location)
            await session.commit()
            await session.refresh(new_location)
            return new_location

async def get_all_vacancies(session: AsyncSession, vacancy_filter: VacancyFilter) -> Sequence[VacancyPublic]:
    statement = vacancy_filter.filter(select(Vacancy).outerjoin(Location))
    result = await session.exec(statement)
    return list(map(VacancyPublic.init_scheme, result.all()))

async def get_vacancy_by_id(id: str, session: AsyncSession) -> VacancyPublic:
    uuid = UUID(id)
    
    statement = select(Vacancy).where(Vacancy.id == uuid).outerjoin(Location)
    
    result = await session.exec(statement)
    result = result.first()
    
    if result is None:
        raise HTTPException(status_code=404, detail="Not Found!")  
    return VacancyPublic.init_scheme(result)

async def create_vacancy(vacancy_to_save: VacancySave, session: AsyncSession) -> VacancyPublic:
    try:
        location = await _get_or_create_location(session, vacancy_to_save.location)
        
        vacancy = vacancy_to_save.to_entity()
        vacancy.location_id = location.id
        vacancy.location = location
        session.add(vacancy)
        await session.commit()
        await session.refresh(vacancy)
        
        return VacancyPublic.init_scheme(vacancy)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Error occurred while saving vacancy! " + \
            "Please inform administration or try later")

    
async def update_vacancy(vacancy_to_update: VacancySave, session: AsyncSession) -> VacancyPublic:
    uuid = UUID(vacancy_to_update.id)
    statement = select(Vacancy).where(Vacancy.id == uuid).outerjoin(Location)
    
    vacancy = await session.exec(statement)
    vacancy = vacancy.first()
    
    if vacancy is None:
        raise HTTPException(status_code=404, detail="Not Found!")
    old_location = vacancy.location
    vacancy = vacancy_to_update.to_entity()
    try:
        if not (vacancy_to_update.location.city == old_location.city or \
                vacancy_to_update.location.region == old_location.region or \
                vacancy_to_update.location.country == old_location.country):
            location = await _get_or_create_location(session, vacancy_to_update.location)
            old_location = location
            vacancy.location_id = location.id
        
        session.add(vacancy)
        await session.commit()
        await session.refresh(vacancy)
        
        vacancy.location = old_location
        
        return VacancyPublic.init_scheme(vacancy)
    except Exception as e:
        
        raise HTTPException(status_code=500, detail="Error occurred while saving vacancy! " + \
            "Please inform administration or try later")
    
async def delete_vacancy(id: str, session: AsyncSession) -> VacancyPublic:
    uuid = UUID(id)
    statement = select(Vacancy).where(Vacancy.id == uuid).outerjoin(Location)
    
    vacancy = await session.exec(statement)
    vacancy = vacancy.first()
    
    if vacancy is None:
        raise HTTPException(status_code=404, detail="Not Found!")
    
    await session.delete(vacancy)
    await session.commit()
    
    
    
            
            
    