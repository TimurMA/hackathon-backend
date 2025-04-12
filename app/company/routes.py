from typing import Sequence

from fastapi import APIRouter
from fastapi_filter import FilterDepends

from app.db import Session

from app.company.schemas import CompanyPublic, CompanySave
from app.vacancy.schemas import CompanyFilter
from app.company.service import *

company_router = APIRouter(
    prefix="/company",
    tags=["Company"]
)

@company_router.get("/all")
async def get_all_companies_async(session: Session, company_filter: CompanyFilter = FilterDepends(CompanyFilter)) -> Sequence[CompanyPublic]:
    return await get_all_companies(session, company_filter)

@company_router.get("/{company_id}")
async def get_company_by_id_async(company_id: str, session: Session) -> CompanyPublic:
    return await get_company_by_id(company_id, session)


@company_router.post("/add")
async def add_company_async(company: CompanySave, session: Session) -> CompanyPublic:
    return await add_company(company, session)


@company_router.put("/update/{company_id}")
async def update_company_async(company_id: str, company: CompanySave, session: Session) -> CompanyPublic:
    return await update_company(company_id, company, session)


@company_router.delete("/delete/{company_id}")
async def delete_company_async(company_id: str, session: Session):
    return await delete_company(company_id, session)

