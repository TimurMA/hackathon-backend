from decimal import Decimal
from typing import Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from docling_core.types.doc.document import DoclingDocument

from app.competence.models import Competence
from app.nlp_document.DocumentReader import DocumentReader
from app.resume.models import ResumeCompetence
from app.resume.schemas import ResumeSave
from app.vacancy.models import Vacancy
from app.vacancy.schemas import VacancyPublic


async def save_resume_and_get_vacancies(file: bytes,
                                        resume_to_save: ResumeSave,
                                        session: AsyncSession,
                                        nlp: DocumentReader) -> Sequence[VacancyPublic]:
    competencies = await session.exec(select(Competence))
    competencies_ids = [competence.id for competence in competencies.all()]

    generic_info = nlp.read_document(file, competencies_ids)

    competencies_info = generic_info[0]
    resume_info = generic_info[1]

    resume = resume_to_save.to_entity()
    resume.phones = resume_info.get("PHONE_NUMBER", [])
    resume.emails = resume_info.get("EMAIL", [])
    resume.urls = resume_info.get("URL", [])

    session.add(resume)
    await session.commit()
    await session.refresh(resume)

    resume_competencies: list[ResumeCompetence] = []
    for (key, val) in competencies_info.items():
        resume_competence = ResumeCompetence(
            competence_id = key,
            level = Decimal(val),
            resume_id = resume.id
        )
        resume_competencies.append(resume_competence)

    session.add_all(resume_competencies)
    await session.commit()

    await session.refresh(resume)

    resume_competencies = resume.competencies

    query = select(Vacancy)
    vacancies = await session.exec(query)
    result: list[VacancyPublic] = []

    for vacancy in vacancies.all():
        vacancy_competence = vacancy.vacancy_competencies
        if len(vacancy_competence) > len(resume_competencies):
            continue
        flag = True
        for vacancy_competence in vacancy_competence:
            flag = any(resume_vacancy.competence_id == vacancy_competence.competence_id and
                       (vacancy_competence.level.normalize() == Decimal("0") or
                        resume_vacancy.level.normalize() >= vacancy_competence.level.normalize())
                       for resume_vacancy in resume_competencies)
            if not flag:
                break
        if flag:
            result.append(VacancyPublic.init_scheme(vacancy))

    return result

