from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import logging

from utils.get_database_url import get_database_url
from app.common_dictionaries import competence_list, competence_contiguity_list
from app.competence.models import Competence, CompetenceContiguity

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
                session.add(Competence(
                    id=competence,
                    name=competence
                ))
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



Session = Annotated[
    AsyncSession,
    Depends(get_session)
]
        
