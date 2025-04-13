from fastapi import APIRouter
from fastapi_filter import FilterDepends

from app.vacancy.service import *
from app.vacancy.schemas import VacancySave, VacancyPublic, VacancyFilter
from app.db import Session

vacancy_router = APIRouter(
    prefix="/vacancy",
    tags=["Vacancy"]
)

@vacancy_router.get("/all")
async def get_all_vacancies_async(session: Session, vacancy_filter: VacancyFilter = FilterDepends(VacancyFilter)) -> Sequence[VacancyPublic]:
    return await get_all_vacancies(session, vacancy_filter)

@vacancy_router.get("/{vacancy_id}")
async def get_vacancy_by_id_async(vacancy_id: str, session: Session) -> VacancyPublic:
    return await get_vacancy_by_id(vacancy_id, session)

@vacancy_router.post("/create")
async def create_vacancy_async(vacancy: VacancySave, session: Session) -> VacancyPublic:
    return await create_vacancy(vacancy, session)

@vacancy_router.put("/update/{vacancy_id}")
async def update_vacancy_async(vacancy_id: str, vacancy: VacancySave, session: Session) -> VacancyPublic:
    return await update_vacancy(vacancy_id, vacancy, session)


@vacancy_router.put("/update/competence/{vacancy_id}")
async def update_vacancy_async(vacancy_id: str, session: Session, vacancy_competence: list[VacancyCompetenceSave] = []) -> Sequence[VacancyCompetencePublic]:
    return await update_vacancy_competencies(vacancy_id, vacancy_competence, session)

@vacancy_router.delete("/delete/{vacancy_id}")
async def delete_vacancy_async(vacancy_id: str, session: Session):
    return await delete_vacancy(vacancy_id, session)