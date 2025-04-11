from typing import Sequence

from fastapi import APIRouter
from fastapi_filter import FilterDepends

from app.db import Session

from app.company.schemas import CompanyPublic, CompanyFilter, CompanySave, CompanyVacancyPublic
from app.company.service import get_company_by_id, get_all_companies, add_company, update_company, delete_company, get_company_vacancies, remove_vacancy_from_company

company_router = APIRouter(
    prefix="/company",
    tags=["Company"]
)


@company_router.get("/{company_id}")
async def get_company_by_id_async(company_id: str, session: Session) -> CompanyPublic:
    return await get_company_by_id(company_id, session)


@company_router.get("/all")
async def get_all_companies_async(session: Session, company_filter: CompanyFilter = FilterDepends(CompanyFilter)) -> Sequence[CompanyPublic]:
    return await get_all_companies(session, company_filter)


@company_router.get("/vacancy/{company_id}")
async def get_company_vacancies_async(company_id: str, session: Session) -> Sequence[CompanyVacancyPublic]:
    return await get_company_vacancies(company_id, session)


@company_router.post("/add")
async def add_company_async(company: CompanySave, session: Session) -> CompanyPublic:
    return await add_company(company, session)


@company_router.put("/update/{company_id}")
async def update_company_async(company_id: str, company: CompanySave, session: Session) -> CompanyPublic:
    return await update_company(company_id, company, session)


@company_router.delete("delete/{company_id}")
async def delete_company_async(company_id: str, session: Session):
    return await delete_company(company_id, session)


@company_router.delete("/delete/{company_id}/{vacancy_id}")
async def remove_vacancy_from_company_async(company_id: str, vacancy_id: str, session: Session):
    return await remove_vacancy_from_company(company_id, vacancy_id, session)
