from typing import TypedDict
from enum import Enum
from src.types import Criterion, QuestionResponse


class Framing(str, Enum):
    STRENGTH = "strength"
    GAPS = "gaps"


class EvaluatedCriterion(TypedDict):
    label: str
    is_satisfied: bool
    points_awarded: int
    reasoning: str


class ClaudeEvaluationResponse(TypedDict):
    criteria: list[EvaluatedCriterion]
    total_score: int
    max_score: int
    summary: str


class CriterionEvaluationResponse(ClaudeEvaluationResponse):
    is_uncertain: bool


def grade_solution(
    question: QuestionResponse, answer: str, rubric: list[Criterion]
) -> CriterionEvaluationResponse:
    """
    build rubric based on the question
    build prompt with strengths framing based on the question
    build prompt with gaps framing based on the question
    pass prompt 1 to claude
    format the response from Claude
    pass prompt 2 to claude
    format the response form Claude
    reconcile the responses
        if both responses have `is_satisfied: true`, then reconcile to true, otherwise false
        take the average of total_score from both responses
        return the gaps framing response
        mark `is_uncertain` to true if the scores are off by more than 5%
    return the response or handle errors
    """
