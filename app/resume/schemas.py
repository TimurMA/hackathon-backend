from sqlmodel import Field, SQLModel
from uuid import UUID
from app.competence.models import CompetenceLevel
from app.resume.models import ResumeBase, Resume, ResumeCompetence
from app.vacancy.models import Vacancy
from app.vacancy.schemas import VacancyPublic


class ResumeCompetencePublic(CompetenceLevel):
    name: str
    id: str
    resume_id: str
    @staticmethod
    def init_scheme(resume_competence: ResumeCompetence):
        return ResumeCompetencePublic(
            id = resume_competence.competence_id,
            name = resume_competence.competence.name,
            level = resume_competence.level,
            resume_id = resume_competence.resume_id
        )

class ResumePublic(ResumeBase):
    id: str
    resume_competencies: list[ResumeCompetencePublic] = Field(default=[])
    vacancy_id: str | None
    vacancy: VacancyPublic | None
    @staticmethod
    def init_scheme(resume: Resume):

        resume_public =  ResumePublic(
            id = resume.id.hex,
            first_name = resume.first_name,
            last_name = resume.last_name,
            emails = resume.emails,
            urls = resume.urls,
            phones = resume.phones,
            resume_competencies = list(map(ResumeCompetencePublic.init_scheme, resume.competencies))
        )

        if resume.vacancy_id:
            resume_public.vacancy_id = resume.vacancy_id.hex
            resume_public.vacancy = VacancyPublic.init_scheme(resume.vacancy)

        return resume_public

class ResumeSave(ResumeBase):
    def to_entity(self):
        return Resume(
            first_name = self.first_name,
            last_name = self.last_name
        )

class ResumeConfirm(SQLModel):
    id: str
    resume_competencies: list[ResumeCompetencePublic] = Field(default=[])
    emails: list[str] = Field(default=[])
    urls: list[str] = Field(default=[])
    phones: list[str] = Field(default=[])

    def convert_resume_competency_to_entity(self) -> list[ResumeCompetence]:
        resume_competencies = []
        for competence in self.resume_competencies:
            resume_competencies.append(ResumeCompetence(
                resume_id = UUID(self.id),
                competence_id = competence.id
            ))
        return resume_competencies





