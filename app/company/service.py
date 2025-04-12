import logging
from typing import Sequence

from sqlalchemy import Select, delete
from fastapi import HTTPException
from sqlmodel import select, cast, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.company.models import Company
from app.company.schemas import CompanyPublic, CompanySave
from app.user.models import User
from app.vacancy.schemas import CompanyFilter

async def get_company_by_id(company_id: str, session: AsyncSession) -> CompanyPublic:
    query = select(Company).where(Company.id == company_id)
    query = cast(Select[Company], query)
    result = await session.exec(query)
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="По результатам запроса ничего не было найдено.")
    return CompanyPublic.init_scheme(company)


async def get_all_companies(session: AsyncSession, company_filter: CompanyFilter) -> Sequence[CompanyPublic]:
    try:
        query = company_filter.filter(select(Company))
        result = await session.exec(query)
        return list(map(CompanyPublic.init_scheme, result.all()))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при получении компаний.")

async def add_company(company_to_save: CompanySave, session: AsyncSession) -> CompanyPublic:
    query = select(Company).where(Company.name == company_to_save.name)
    query = cast(Select[Company], query)
    existing_company = await session.exec(query)
    if existing_company.first():
        await session.rollback()
        raise HTTPException(status_code=400, detail="Компания с таким названием уже существует.")

    hr = None
    if company_to_save.hr_id is not None:
        try:
            hr = await session.get(User, {"id": company_to_save.hr_id})
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=400, detail="Bad hr_id")

    if hr is None:
        raise HTTPException(status_code=404, detail="HR не найден")

    try:

        company = company_to_save.to_entity()

        company.hr_id = hr.id

        session.add(company)
        await session.commit()
        await session.refresh(company)
        return CompanyPublic.init_scheme(company)
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при добавлении компании.")


async def update_company(company_id: str, company_to_update: CompanySave, session: AsyncSession) -> CompanyPublic:
    query = select(Company).where(Company.id == company_id)
    query = cast(Select[Company], query)
    result = await session.exec(query)
    company = result.scalar_one_or_none()

    hr: User | None = None
    if company_to_update.hr_id is not None:
        try:
            hr = await session.get(User, {"id": company_to_update.hr_id})
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=400, detail="Bad hr Id")

    if hr is None:
        raise HTTPException(status_code=404, detail="HR не найден")


    if not company:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Компания не найдена.")
    if company.name != company_to_update.name:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Компания с таким названием уже существует.")
    try:
        company.name = company_to_update.name
        company.hr_id = hr.id

        session.add(company)
        await session.commit()
        await session.refresh(company)
        return CompanyPublic.init_scheme(company)
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при обновлении компании.")


async def delete_company(company_id: str, session: AsyncSession):
    query = select(Company).where(Company.id == company_id)
    query = cast(Select[Company], query)
    result = await session.exec(query)
    company = result.scalar_one_or_none()
    if not company:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Компания не найдена.")
    try:
        await session.delete(company)
        await session.commit()
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при удалении компании.")

