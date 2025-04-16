import logging
from fastapi import HTTPException
from typing import cast

from sqlalchemy import Select
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.test.models import Test
from app.test.schemas import TestPublic


async def get_all_tests_by_company_id(company_id: str, session: AsyncSession):
    query = select(Test).where(Test.company_id == company_id)
    result = await session.exec(cast(Select[Test], query))
    return list(map(TestPublic.init_scheme, result.all()))


async def get_test_by_id(test_id: str, session: AsyncSession):
    query = select(Test).where(Test.id == test_id)

    try:
        result = await session.exec(cast(Select[Test], query))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка! Сообщите администратору или повторите позже")

    test = result.first()
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден!")
    
    return TestPublic.init_scheme(test)


