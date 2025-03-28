from typing import Annotated, Any, AsyncGenerator
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from utils.get_database_url import get_database_url

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
        
Session = Annotated[
    AsyncSession,
    Depends(get_session)
]
        
