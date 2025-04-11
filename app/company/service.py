import logging
from typing import Sequence

from sqlalchemy import Select, delete
from fastapi import HTTPException
from sqlmodel import select, cast, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.company.models import Company, CompanyVacancy
from app.company.schemas import CompanyPublic, CompanyFilter, CompanySave, CompanyVacancyPublic
from app.user.models import User
from app.vacancy.models import Vacancy


async def __add_vacancy_to_company(company_id: str, vacancy_id: str, session: AsyncSession) -> CompanyVacancyPublic:
    vacancy = await session.get(Vacancy, vacancy_id)
    if not vacancy:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Вакансия не найдена.")
    company = await session.get(Company, company_id)
    if not company:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Компания не найдена.")
    query = select(CompanyVacancy).where(and_(
        CompanyVacancy.company_id == company_id,
        CompanyVacancy.vacancy_id == vacancy_id)
    )
    existing = await session.exec(query)
    if existing.first():
        await session.rollback()
        raise HTTPException(status_code=400, detail="Такая вакансия уже привязана к компании.")
    try:
        company_vacancy = CompanyVacancy(
            company_id=company_id,
            vacancy_id=vacancy_id
        )
        session.add(company_vacancy)
        await session.commit()
        await session.refresh(company_vacancy)
        return CompanyVacancyPublic.init_scheme(company_vacancy)
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при добавлении вакансии к компании.")


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


async def get_company_vacancies(company_id: str, session: AsyncSession) -> Sequence[CompanyVacancyPublic]:
    try:
        query = select(CompanyVacancy).where(CompanyVacancy.company_id == company_id)
        result = await session.exec(query)
        return list(map(CompanyVacancyPublic.init_scheme, result.all()))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при получении вакансий компании.")


async def add_company(company_to_save: CompanySave, session: AsyncSession) -> CompanyPublic:
    query = select(Company).where(Company.name == company_to_save.name)
    query = cast(Select[Company], query)
    existing_company = await session.exec(query)
    if existing_company.first():
        await session.rollback()
        raise HTTPException(status_code=400, detail="Компания с таким названием уже существует.")
    try:
        company = company_to_save.to_entity()
        if company_to_save.hr_id:
            hr = await session.get(User, company_to_save.hr_id)
            if not hr:
                await session.rollback()
                raise HTTPException(status_code=404, detail="Пользователь не найден.")
            company.HR = hr
        session.add(company)
        await session.commit()
        await session.refresh(company)
        if company_to_save.vacancies:
            for vacancy_data in company_to_save.vacancies:
                await __add_vacancy_to_company(company.id, vacancy_data.vacancy_id, session)
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
    if not company:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Компания не найдена.")
    if company.name != company_to_update.name:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Компания с таким названием уже существует.")
    try:
        company.name = company_to_update.name
        if company_to_update.hr_id:
            hr = await session.get(User, company_to_update.hr_id)
            if not hr:
                await session.rollback()
                raise HTTPException(status_code=404, detail="Пользователь не найден.")
            company.HR = hr
        else:
            company.HR = None
        if company_to_update.vacancies:
            await session.exec(
                delete(CompanyVacancy).where(CompanyVacancy.company_id == company_id)
            )
            for vacancy_data in company_to_update.vacancies:
                await __add_vacancy_to_company(company_id, vacancy_data.vacancy_id, session)
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


async def remove_vacancy_from_company(company_id: str, vacancy_id: str, session: AsyncSession):
    query = select(CompanyVacancy).where(and_(
        CompanyVacancy.company_id == company_id,
        CompanyVacancy.vacancy_id == vacancy_id)
    )
    result = await session.exec(query)
    company_vacancy = result.scalar_one_or_none()
    if not company_vacancy:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Такой вакансии нет в этой комапнии.")
    try:
        await session.delete(company_vacancy)
        await session.commit()
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка при удалении вакансии из компании.")
