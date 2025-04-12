from app.db import Session
from app.competence.service import *
from app.competence.schemas import CompetencePublic, CompetenceFilter, CompetenceSave

from fastapi import APIRouter
from fastapi_filter import FilterDepends


competence_router = APIRouter(
    prefix="/competence",
    tags=["Competence"]
)

@competence_router.get("/all")
async def get_all_competence_async(session: Session, skill_filter: CompetenceFilter = FilterDepends(CompetenceFilter)) -> Sequence[CompetencePublic]:
    return await get_all_competence(session, skill_filter)

@competence_router.get("/{competence_id}")
async def get_competence_by_id_async(competence_id: str, session: Session) -> CompetencePublic:
    return await get_competence_by_id(competence_id, session)


@competence_router.post("/add")
async def add_competence_async(competence: CompetenceSave, session: Session) -> CompetencePublic:
    return await add_competence(competence, session)


@competence_router.put("/update/{competence_id}")
async def update_competence_async(competence_id: str, competence: CompetenceSave, session: Session) -> CompetencePublic:
    return await update_competence(competence_id, competence, session)


@competence_router.delete("/delete/{competence_id}")
async def delete_competence_async(competence_id: str, session: Session):
    return await delete_competence(competence_id, session)
