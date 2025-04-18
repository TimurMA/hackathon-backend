from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import logging

from app.company.models import Company
from app.vacancy.models import Location, Vacancy
from utils.get_database_url import get_database_url
from app.common_dictionaries import competence_contiguity_list, competence_list, company, vacancy_list, location_list
from app.competence.models import CompetenceContiguity

DATABASE_URL = get_database_url()

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

async def init_db():
    engine.begin()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        
async def close_connection():
    await engine.dispose()

async def init_common_competencies():
    async with async_session() as session:
        competencies = competence_list.copy()
        for competence in competencies:
            try:
                session.add(competence)
                await session.commit()
            except Exception as e:
                logging.error(e)
                await session.rollback()

async def init_competence_contiguity():
    def change_first_and_second(ca: CompetenceContiguity):
        new_ca = CompetenceContiguity(
            first_competence_id = ca.second_competence_id,
            second_competence_id = ca.first_competence_id,
            contiguity_coefficient = ca.contiguity_coefficient
        )
        return new_ca

    async with async_session() as session:
        for competence_contiguity in competence_contiguity_list:
            try:
                session.add(competence_contiguity)
                session.add(change_first_and_second(competence_contiguity))
                await session.commit()

            except Exception as e:
                logging.error(e)
                await session.rollback()

async def init_company_with_vacancies():
    async with async_session() as session:
        exist = await session.execute(select(Company).where(Company.name == company.name))
        exist = exist.one_or_none()
        if not exist:
            try:
                session.add(company)
                await session.commit()
                await session.refresh(company)
                company_id = company.id
            except Exception as e:
                logging.error(e)
                await session.rollback()
        else:
            exist_company, = exist
            company_id = exist_company.id
        for location in location_list:
            try:
                session.add(location)
                await session.commit()
                await session.refresh(location)
            except Exception as e:
                logging.error(e)
                await session.rollback()
        location_ids = []
        for location in location_list:
            try:
                query = select(Location.id).where(
                    Location.region == location.region,
                    Location.country == location.country,
                    Location.city == location.city
                )
                l = await session.execute(query)
                location_ids.append(l.one()[0])
            except Exception as e:
                logging.error(e)

    vc = []

    for location_id in location_ids:
        for vacancy_dict in vacancy_list:
            vacancy = Vacancy(
                name = vacancy_dict.get("name"),
                url=vacancy_dict.get("url"),
                description=vacancy_dict.get("description"),
            )
            vacancy.company_id = company_id
            vacancy.location_id = location_id

            query = select(Vacancy).where(
                Vacancy.name == vacancy.name,
                Vacancy.url == vacancy.url,
                Vacancy.description == vacancy.description
            )

            result = await session.execute(query)
            current_vacancy = result.one_or_none()

            if current_vacancy is None:
                try:
                    session.add(vacancy)
                    await session.commit()
                    await session.refresh(vacancy)
                except Exception as e:
                    logging.error(e)
            else:
                vacancy = current_vacancy

            for competence in vacancy_dict.get("vacancy_competencies"):
                try:
                    competence.vacancy_id = vacancy.id
                    session.add(competence)
                    await session.commit()
                except Exception as e:
                    logging.error(e)
                    await session.rollback()




Session = Annotated[
    AsyncSession,
    Depends(get_session)
]
        
