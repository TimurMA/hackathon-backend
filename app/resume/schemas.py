from app.competence.models import CompetenceLevel
from app.resume.models import ResumeBase, Resume, ResumeCompetence


class ResumeCompetencePublic(CompetenceLevel):
    name: str
    id: str

    @staticmethod
    def init_scheme(resume_competence: ResumeCompetence):
        return ResumeCompetencePublic(
            id = resume_competence.competence_id,
            name = resume_competence.competence.name,
            level = resume_competence.level
        )

class ResumePublic(ResumeBase):
    id: str
    competencies: list[ResumeCompetencePublic]

    @staticmethod
    def init_scheme(resume: Resume):
        return ResumePublic(
            id = resume.id.hex,
            first_name = resume.first_name,
            last_name = resume.last_name,
            emails = resume.emails,
            urls = resume.urls,
            phones = resume.phones,
            competencies = list(map(ResumeCompetencePublic.init_scheme, resume.competencies))
        )

class ResumeSave(ResumeBase):
    def to_entity(self):
        return Resume(
            first_name = self.first_name,
            last_name = self.last_name
        )




