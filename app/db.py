from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import logging

from utils.get_database_url import get_database_url
from app.common_dictionaries import competence_list
from app.competence.models import Competence

DATABASE_URL = get_database_url()

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async def init_db():
    engine.begin()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        
async def close_connection():
    await engine.dispose()

async def init_common_competencies():
    session = await get_session().__anext__()
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
    await session.close()


        
Session = Annotated[
    AsyncSession,
    Depends(get_session)
]
        
