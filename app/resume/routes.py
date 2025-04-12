from fastapi import APIRouter, UploadFile, File, Form

from app.db import Session
from app.nlp import Reader
from app.resume.service import *

resume_router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

@resume_router.post('/add')
async def save_resume_info_and_get_vacancies(session: Session,
                                             nlp: Reader,
                                             file: UploadFile = File(...),
                                             user_info: str = Form(...)
                                             ) -> Sequence[VacancyPublic]:
    b =  await file.read()
    resume_to_save = ResumeSave.model_validate_json(user_info)
    return await save_resume_and_get_vacancies(b, resume_to_save, session, nlp)
