from fastapi import APIRouter, UploadFile, File, Form

from app.db import Session
from app.nlp import Reader
from app.resume.service import *
from app.vacancy.schemas import VacancyPublic
from app.resume.schemas import ResumeConfirm

resume_router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

@resume_router.post('/read')
async def read_resume(session: Session,
                      nlp: Reader,
                      file: UploadFile = File(...),
                      user_info: str = Form(...)) -> ResumePublic:
    b =  await file.read()
    resume_to_save = ResumeSave.model_validate_json(user_info)
    return await save_resume_and_send_to_confirm_competencies_and_info(b, resume_to_save, session, nlp)

@resume_router.put('confirm')
async def confirm_resume(session: Session, resume_to_confirm: ResumeConfirm) -> Sequence[VacancyPublic]:
    return confirm_resume_and_send_vacancies(session, resume_to_confirm)