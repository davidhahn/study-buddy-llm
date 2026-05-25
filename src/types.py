from typing import TypedDict, Literal, NotRequired
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
    prompt: str
    constraints: list[str]
    examples: list[ExampleResponse]
    setup_code: str | None
