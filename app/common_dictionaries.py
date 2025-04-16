from decimal import Decimal
from app.competence.models import CompetenceContiguity

competence_list=[
    "SQL",
    "NoSQL",
    "parallel processing",
    "Hadoop",
    "data buses",
    "data preprocessing",
    "data streaming",
    "ML on big data",
    "working with a distributed cluster system",
    "parallel computing to speed up ML",
    "reinforcement learning",
    "the basics of deep learning",
    "ML for generation image and video",
    "ML for generation natural language",
    "NLP",
    "Image and video analysis",
    "recommendation systems",
    "information search",
    "optimization methods",
    "ML methods",
    "Programming language",
    "evaluating the work of Al methods",
    "statistical methods",
    "methodology for developing Al solutions",
    "trends AI",
]

competence_contiguity_list = [
    CompetenceContiguity(
        first_competence_id = "ML for generation image and video",
        second_competence_id = "Image and video analysis",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML for generation natural language",
        second_competence_id = "NLP",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "the basics of deep learning",
        second_competence_id = "ML methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "reinforcement learning",
        second_competence_id = "the basics of deep learning",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML methods",
        second_competence_id = "statistical methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML methods",
        second_competence_id = "optimization methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML methods",
        second_competence_id = "evaluating the work of Al methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "parallel computing to speed up ML",
        second_competence_id = "parallel processing",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML for generation image and video",
        second_competence_id = "the basics of deep learning",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML for generation natural language",
        second_competence_id = "the basics of deep learning",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "Image and video analysis",
        second_competence_id = "ML methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "NLP",
        second_competence_id = "ML methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML on big data",
        second_competence_id = "ML methods",
        contiguity_coefficient = Decimal("1")
    )
]