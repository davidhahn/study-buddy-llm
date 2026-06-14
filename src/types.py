from typing import TypedDict, Literal, NotRequired
import datetime
from enum import Enum


class ExerciseType(str, Enum):
    ALGORITHM = "algorithm"
    UI_COMPONENT = "ui_component"
    ASYNC = "async"


class Language(str, Enum):
    JAVASCRIPT = "javascript"
    PYTHON = "python"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXTREME = "extremely hard"


class ExampleResponse(TypedDict):
    input: str
    output: str
    explanation: str


class Criterion(TypedDict):
    id: str
    label: str
    points: int
    description: str
    evaluation_type: Literal["independent", "cascading"]
    evaluation_dependency: NotRequired[str]


class Topic(str, Enum):
    PRACTICAL_PROBLEMS = "Practical Problems"
    BINARY_SEARCH_TREE = "Binary Search Tree"
    TREES = "Trees"
    TRIES = "Tries"
    GRAPHS = "Graphs"
    ARRAYS = "Arrays"
    STRINGS = "Strings"


class QuestionResponse(TypedDict):
    topic: Topic
    difficulty: Difficulty
    exercise_type: ExerciseType
    language: Language
    prompt: str
    constraints: list[str]
    examples: list[ExampleResponse]
    setup_code: str | None


class GeneratedProblem(TypedDict):
    question: QuestionResponse
    problem_id: int


class EvaluatedCriterion(TypedDict):
    id: str
    label: str
    is_satisfied: bool
    points_awarded: int
    reasoning: str


class ClaudeEvaluationResponse(TypedDict):
    criteria: list[EvaluatedCriterion]
    total_score: float
    max_score: int
    summary: str


class CriterionEvaluationResponse(ClaudeEvaluationResponse):
    is_uncertain: bool


class ProblemRow(TypedDict):
    id: int
    topic: str
    difficulty: Difficulty
    exercise_type: ExerciseType
    language: Language
    prompt: str
    constraints: str
    examples: str
    setup_code: str | None
    interval: int | None
    ease_factor: float | None
    repetitions: int | None
    next_review_date: datetime.datetime | None
    created_at: datetime.datetime


class TopicSuggestion(TypedDict):
    id: int
    name: str
    slug: str
    problems: list[ProblemRow]
    explanation: str
