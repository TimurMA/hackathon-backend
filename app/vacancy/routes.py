from typing import Sequence
from fastapi import APIRouter
from fastapi_filter import FilterDepends

from app.vacancy.schemas import VacancySave, VacancyPublic, VacancyFilter
from app.vacancy.service import *
from app.db import Session

vacancy = APIRouter(
    prefix="/vacancy",
    tags=["Vacancy"]
)

@vacancy.get("/all")
async def get_all_vacancies_async(session: Session, vacancy_filter: VacancyFilter = FilterDepends(VacancyFilter)) -> Sequence[VacancyPublic]:
    return await get_all_vacancies(session, vacancy_filter)

@vacancy.get("/{id}")
async def get_vacancy_by_id_async(id: str, session: Session) -> VacancyPublic:
    return await get_vacancy_by_id(id, session)
    

@vacancy.post("/create")
async def create_vacancy_async(vacancy: VacancySave, session: Session) -> VacancyPublic:
    return await create_vacancy(vacancy, session)

@vacancy.put("/update")
async def update_vacancy_async(vacancy: VacancySave, session: Session) -> VacancyPublic:
    return await update_vacancy(vacancy, session)

@vacancy.delete("/{str}")
async def delete_vacancy_async(id: str, session: Session):
    return await delete_vacancy(id, session)