import logging

from typing import Sequence, cast
from fastapi import HTTPException
from sqlalchemy import Select
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.vacancy.models import Vacancy, Location
from app.vacancy.schemas import VacancyPublic, VacancyFilter, VacancySave, LocationSave, LocationPublic

async def _get_or_create_location(session: AsyncSession, location_data: LocationSave) -> Location:
        statement = select(Location).where(
                Location.country == location_data.country,
                Location.region == location_data.region,
                Location.city == location_data.city
            )

        statement = cast(Select[Location], statement)

        existing = await session.exec(statement)
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

async def get_vacancy_by_id(vacancy_id: str, session: AsyncSession) -> VacancyPublic:
    statement = select(Vacancy).where(Vacancy.id == vacancy_id).outerjoin(Location)
    
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
        raise HTTPException(status_code=500, detail="Error occurred while saving vacancy! " +
                                                    "Please inform administration or try later")

async def update_vacancy(vacancy_id: str, vacancy_to_update: VacancySave, session: AsyncSession) -> VacancyPublic:
    statement = select(Vacancy).where(Vacancy.id == vacancy_id).outerjoin(Location)

    vacancy = await session.exec(statement)
    vacancy = vacancy.one()
    print(vacancy)
    if vacancy is None:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Not Found!")

    location = vacancy.location
    try:
        if not (vacancy_to_update.location.city == location.city or
                vacancy_to_update.location.region == location.region or
                vacancy_to_update.location.country == location.country):

            location = await _get_or_create_location(session, vacancy_to_update.location)

        vacancy.location_id = location.id
        vacancy.url = vacancy_to_update.url
        vacancy.name = vacancy_to_update.name
        vacancy.description = vacancy_to_update.description

        session.add(vacancy)
        await session.commit()
        await session.refresh(vacancy)
        
        return VacancyPublic.init_scheme(vacancy)
    except Exception as e:
        logging.error(e)
        await session.rollback()
        raise HTTPException(status_code=500, detail="Error occurred while saving vacancy! " +
                                                    "Please inform administration or try later")
    
async def delete_vacancy(vacancy_id: str, session: AsyncSession):
    statement = select(Vacancy).where(Vacancy.id == vacancy_id).outerjoin(Location)
    
    vacancy = await session.exec(statement)
    vacancy = vacancy.first()
    
    if vacancy is None:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Not Found!")
    
    try:
        await session.delete(vacancy)
        await session.commit()
    except Exception as e:
        logging.error(e)
        await session.rollback()
        raise HTTPException(status_code=500, detail="Error occurred while saving vacancy! " +
                                                    "Please inform administration or try later")
    
    
    
            
            
    