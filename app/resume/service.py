import logging

from typing import Sequence, cast
from fastapi import HTTPException
from sqlalchemy import Select
from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession

from app.competence.models import Competence, CompetenceContiguity
from app.nlp_document.DocumentReader import DocumentReader
from app.resume.models import ResumeCompetence, Resume
from app.resume.schemas import ResumeSave, ResumePublic, ResumeCompetencePublic, ResumeConfirm
from app.vacancy.models import Vacancy
from app.vacancy.schemas import VacancyPublic


async def save_resume_and_send_to_confirm_competencies_and_info(file: bytes,
                                        resume_to_save: ResumeSave,
                                        session: AsyncSession,
                                        nlp: DocumentReader) -> ResumePublic:
    competencies = await session.exec(select(Competence))
    competencies_ids = [competence.id for competence in competencies.all()]

    try:
        generic_info = nlp.read_document(file, competencies_ids)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Не удалось прочитать ваше резюме")

    competencies_info = generic_info[0]
    resume_info = generic_info[1]

    resume = resume_to_save.to_entity()
    resume.phones = resume_info.get("PHONE_NUMBER", [])
    resume.emails = resume_info.get("EMAIL", [])
    resume.urls = resume_info.get("URL", [])

    try:
        session.add(resume)
        await session.commit()
        await session.refresh(resume)
    except Exception as e:
        await session.rollback()
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка! Сообщите администрации или повторите позже")

    resume_competencies = []
    for (key, val) in competencies_info.items():
        resume_competence = ResumeCompetencePublic(
            id = key,
            name=val,
            level=float('0'),
            resume_id=resume.id
        )
        resume_competencies.append(resume_competence)

    result = ResumePublic.init_scheme(resume)
    result.resume_competencies = resume_competencies
    return result

async def confirm_resume_and_send_vacancies(session: AsyncSession, resume_to_confirm: ResumeConfirm) -> Sequence[VacancyPublic]:
    query = select(Resume).where(Resume.id == resume_to_confirm.id)

    try:
        resumes = await session.exec(cast(Select[Resume], query))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка! Сообщите администрации или повторите позже")

    resume = resumes.first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume не найдено")

    resume.emails = resume_to_confirm.emails
    resume.phones = resume_to_confirm.phones
    resume.urls = resume_to_confirm.urls

    try:
        session.add(resume)
        await session.commit()
        await session.refresh(resume)
    except Exception as e:
        logging.error(e)
        await session.rollback()
        raise HTTPException(status_code=500, detail="Ошибка! Сообщите администрации или повторите позже")

    try:
        resume_competence_to_save = resume_to_confirm.convert_resume_competency_to_entity()
        session.add_all(resume_competence_to_save)

        await session.commit()

        for rc in resume_competence_to_save:
            await session.refresh(rc)

    except Exception as e:
        logging.error(e)
        await session.rollback()
        raise HTTPException(status_code=500, detail="Ошибка! Сообщите администрации или повторите позже")

    resume_competence_ids = [competence.competence_id for competence in resume_competence_to_save]

    query = (
        select(Competence.id).join(
            CompetenceContiguity,
            Competence.id == CompetenceContiguity.second_competence_id
        ).where(col(CompetenceContiguity.first_competence_id).in_(resume_competence_ids))
    )

    extra_competence_ids = await session.exec(query)

    resume_competence_ids.extend(extra_competence_ids)

    try:
        query = select(Vacancy)
        vacancies = await session.exec(query)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Ошибка! Сообщите администрации или повторите позже")
    result: list[VacancyPublic] = []

    for vacancy in vacancies.all():
        vacancy_competence_ids = [vacancy_competence.competence_id for vacancy_competence in vacancy.vacancy_competencies]
        if len(vacancy_competence_ids) > len(resume_competence_ids):
            continue
        flag = True
        for vacancy_competence_id in vacancy_competence_ids:
            flag = any([vacancy_competence_id == competence_id for competence_id in resume_competence_ids])
            if not flag:
                break
        if flag:
            result.append(VacancyPublic.init_scheme(vacancy))

    return result

