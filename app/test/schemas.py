from sqlmodel import Field, SQLModel
from uuid import UUID

from app.company.schemas import CompanyPublic
from app.resume.schemas import ResumePublic
from app.test.models import TestBase, QuestionBase, AnswerBase, Answer, ChoiceBase, Choice, Question, Test, \
    TestResultBase, TestResult
from app.vacancy.schemas import VacancyCompetencePublic

class ChoicePublic(ChoiceBase, AnswerBase):
    answer_id: str
    test_result_id: str
    question_id: str

    @staticmethod
    def init_scheme(choice: Choice):
        return ChoicePublic(
            answer_id = choice.answer_id,
            test_result_id = choice.test_result_id,
            question_id = choice.answer.question_id,
            answer = choice.answer.answer,
            is_selected = choice.is_selected,
        )

class ChoiceSave(ChoiceBase):
    answer_id: str
    test_result_id: str

    def to_entity(self):
        return Choice(
            answer_id = UUID(self.answer_id),
            test_result_id = UUID(self.test_result_id),
            is_selected = self.is_selected
        )

class AnswerPublic(AnswerBase):
    id: str
    question_id: str

    @staticmethod
    def init_scheme(answer: Answer):
        return AnswerPublic(
            id = answer.id.hex,
            question_id = answer.question_id.hex,
            answer = answer.answer,
            value = answer.value
        )

class AnswerSave(AnswerBase):
    question_id: str

    def to_entity(self):
        return Answer(
            question_id = UUID(self.question_id),
            answer = self.answer,
            value = self.value
        )

class QuestionPublic(QuestionBase):
    id: str
    test_id: str

    answers: list["AnswerPublic"] | list["ChoicePublic"] = Field(default=[])

    @staticmethod
    def init_scheme(question: Question):
        return QuestionPublic(
            id = question.id.hex,
            question = question.question,
            test_id = question.test_id,
            q_type = question.q_type,
            answers = list(map(AnswerPublic.init_scheme, question.answers))
        )

    @staticmethod
    def init_scheme_for_test_result(choices: list[ChoicePublic], question: Question):
        question = QuestionPublic.init_scheme(question)
        question.answers = choices
        return question

class QuestionSave(QuestionBase):
    test_id: str
    answers: list[AnswerSave]

    def to_entity(self):
        return Question(
            test_id = UUID(self.test_id),
            q_type = self.q_type,
            question = self.question,
            answers = [answer.to_entity() for answer in self.answers]
        )

class TestResultPublic(TestBase, TestResultBase):
    id: str
    test_id: str
    resume_id: str

    resume: ResumePublic
    questions: list["QuestionPublic"]

    @staticmethod
    def init_scheme(test: TestResult):
        choices = list(map(ChoicePublic.init_scheme, test.choices))
        return TestResultPublic(
            id = test.id.hex,
            test_id = test.test_id.hex,
            resume_id = test.resume_id.hex,
            resume = ResumePublic.init_scheme(test.resume),
            questions = [QuestionPublic.init_scheme_for_test_result(
                choices=list(filter(lambda choice: choice.question_id == question.id.hex, choices)),
                question=question
            ) for question in test.test.questions],
            started_at = test.started_at,
            finished_at = test.finished_at,
            max_result = test.max_result,
            result = test.result,
            test_time = test.test.test_time,
            name = test.test.name
        )

class TestResultSave(SQLModel):
    test_id: str
    resume_id: str
    def to_entity(self):
        return TestResult(
            test_id = UUID(self.test_id),
            resume_id = UUID(self.resume_id),
            result = 0
        )

class TestPublic(TestBase):
    id: str
    company_id: str

    company: CompanyPublic
    vacancy_competence: list[VacancyCompetencePublic] = Field(default=list)

    @staticmethod
    def init_scheme(test: Test):
        return TestResult(
            id = test.id.hex,
            name = test.name,
            test_time = test.test_time,
            company = test.company,
            vacancy_competence = list(map(VacancyCompetencePublic.init_scheme, test.vacancy_competencies))
        )

class TestSave(TestBase):
    company_id: str

    questions: list[QuestionSave] = Field(default=[])

    def to_entity(self):
        return Test(
            name = self.name,
            test_time = self.test_time,
            company_id = self.company_id,
            questions = [question.to_entity() for question in self.questions]
        )


