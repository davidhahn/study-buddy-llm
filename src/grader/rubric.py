from typing import TypedDict
from enum import Enum


class ExerciseType(str, Enum):
    ALGORITHM = "algorithm"
    UI_COMPONENT = "ui_component"
    ASYNC = "async"


class Language(str, Enum):
    JAVASCRIPT = "javascript"
    PYTHON = "python"


class Criterion(TypedDict):
    label: str
    points: int
    description: str


BASE_RUBRIC: list[Criterion] = [
    {
        "label": "Correct output",
        "points": 3,
        "description": "Produces the right result for the primary use case described in the problem.",
    },
    {
        "label": "Edge cases handled",
        "points": 2,
        "description": "Handles empty input, null/None, zero, or boundary values without crashing or returning wrong output.",
    },
    {
        "label": "Clear naming",
        "points": 1,
        "description": "Variable and function names describe what they hold or do. Single-letter names only acceptable as loop counters in simple iterations.",
    },
    {
        "label": "No unnecessary nesting",
        "points": 1,
        "description": "Conditionals not nested more than 2 levels deep. Guard clauses used to handle invalid input early.",
    },
    {
        "label": "No dead code",
        "points": 1,
        "description": "No unused variables, unreachable branches, or commented-out code blocks.",
    },
    {
        "label": "Single responsibility",
        "points": 1,
        "description": "Each function does one describable thing. If a function needs 'and' to describe it, it should be split.",
    },
    {
        "label": "Modular and extensible",
        "points": 2,
        "description": "Adding a related feature should not require rewriting existing logic — only adding to it.",
    },
    {
        "label": "No unnecessary complexity overhead",
        "points": 1,
        "description": "If a simpler approach has the same Big-O complexity, it is preferred. Only flag performance if a significantly better complexity class is straightforward.",
    },
]

EXERCISE_RUBRICS: dict[ExerciseType, list[Criterion]] = {
    ExerciseType.ALGORITHM: [
        {
            "label": "Correct time complexity",
            "points": 2,
            "description": "Solution achieves the expected Big-O time complexity. Flag only if a significantly better complexity class is straightforward.",
        },
        {
            "label": "Correct space complexity",
            "points": 1,
            "description": "Solution does not allocate unnecessary data structures. Auxiliary space is proportional to what the algorithm genuinely requires.",
        },
        {
            "label": "No off-by-one errors",
            "points": 1,
            "description": "Loop boundaries, array indices, and slice ranges are correct. Check start/end conditions explicitly.",
        },
        {
            "label": "Terminates correctly",
            "points": 1,
            "description": "Recursive solutions have a clear base case. Iterative solutions cannot infinite-loop on valid input.",
        },
        {
            "label": "Data structure choice is justified",
            "points": 1,
            "description": "The chosen data structure suits the access patterns of the problem.",
        },
    ],
    ExerciseType.UI_COMPONENT: [
        {
            "label": "Props / inputs are minimal and typed",
            "points": 1,
            "description": "Component accepts only what it needs. Props are clearly named and typed correctly.",
        },
        {
            "label": "State is local where possible",
            "points": 1,
            "description": "State is not lifted higher than necessary. Only state that genuinely needs to be shared is elevated.",
        },
        {
            "label": "Handles loading and error states",
            "points": 2,
            "description": "Component renders meaningful loading and error states — not simply None or a blank render.",
        },
        {
            "label": "No logic in the render / return",
            "points": 1,
            "description": "Business logic and data transformation happen outside the template. The return block should be declarative.",
        },
        {
            "label": "Accessible markup",
            "points": 1,
            "description": "Interactive elements use semantic HTML. Images have alt text. Form inputs have labels.",
        },
        {
            "label": "No hardcoded values in render",
            "points": 1,
            "description": "Strings, colors, sizes, and magic numbers are not inline in the markup.",
        },
    ],
    ExerciseType.ASYNC: [
        {
            "label": "Errors are caught and handled",
            "points": 2,
            "description": "All async operations are wrapped in try/except. Errors are not silently swallowed.",
        },
        {
            "label": "No unhandled exceptions in coroutines",
            "points": 2,
            "description": "Every awaitable that can raise is inside a try/except or has explicit error handling. Unawaited coroutines are not present.",
        },
        {
            "label": "No unnecessary sequential awaits",
            "points": 1,
            "description": "Independent async operations run concurrently with asyncio.gather(). Sequential awaits only where one operation genuinely depends on the previous result.",
        },
        {
            "label": "Loading and error state are tracked",
            "points": 1,
            "description": "The caller can determine whether the operation is in-flight, succeeded, or failed.",
        },
        {
            "label": "No race conditions",
            "points": 1,
            "description": "If concurrent tasks write shared state, appropriate locks or task-safe patterns are used.",
        },
    ],
}

LANGUAGE_RUBRICS: dict[Language, list[Criterion]] = {
    Language.JAVASCRIPT: [
        {
            "label": "Correct use of const/let",
            "points": 1,
            "description": "No var. let only where reassignment actually occurs. const everywhere else.",
        },
        {
            "label": "No input mutation",
            "points": 1,
            "description": "Functions do not modify arrays or objects passed as arguments unless mutation is explicitly the stated purpose.",
        },
        {
            "label": "Destructuring used where it improves clarity",
            "points": 1,
            "description": "Object and array destructuring preferred over repeated property access where it aids readability.",
        },
        {
            "label": "No implicit type coercion",
            "points": 1,
            "description": "Strict equality (===) used throughout. No reliance on truthy/falsy coercion where an explicit check is clearer.",
        },
    ],
    Language.PYTHON: [
        {
            "label": "Follows PEP 8 naming conventions",
            "points": 1,
            "description": "Variables and functions use snake_case. Classes use PascalCase. Constants use UPPER_SNAKE_CASE.",
        },
        {
            "label": "Uses Pythonic idioms where appropriate",
            "points": 1,
            "description": "List comprehensions preferred over manual appends for simple cases. enumerate() over range(len()). zip() for parallel iteration.",
        },
        {
            "label": "No bare except clauses",
            "points": 1,
            "description": "Except clauses catch specific exception types. Bare except: or except Exception: without re-raising or logging is a flag.",
        },
        {
            "label": "Type hints used on function signatures",
            "points": 1,
            "description": "Function parameters and return types are annotated. Internal variable hints are optional.",
        },
        {
            "label": "No mutable default arguments",
            "points": 1,
            "description": "def func(data=[]) and def func(config={}) are bugs. Mutable defaults should use None with an explicit check inside the body.",
        },
    ],
}


def build_rubric(
    exercise_type: ExerciseType,
    language: Language,
) -> list[Criterion]:
    return [
        *BASE_RUBRIC,
        *EXERCISE_RUBRICS[exercise_type],
        *LANGUAGE_RUBRICS[language],
    ]


# def format_rubric(criteria: list[Criterion]) -> str:
#     return "\n".join(
#         f"{i + 1}. {c.label} ({c.points} pt): {c.description}"
#         for i, c in enumerate(criteria)
#     )


# def build_judge_prompt(inputs: JudgePromptInputs) -> str:
#     include_base = (
#         inputs.include_base_rubric
#         and inputs.exercise_type != ExerciseType.SYSTEM_DESIGN
#     )
#     criteria = build_rubric(inputs.exercise_type, inputs.language, include_base)
#     max_score = sum(c.points for c in criteria)

#     return f"""You are an objective evaluator for a coding study application. \
# Your job is to assess a learner's answer against a reference answer using a specific rubric.

# Do not be lenient. Do not reward effort or length. Evaluate only what is stated in the rubric.

# ## Question
# {inputs.question}

# ## Reference answer
# {inputs.reference_answer}

# ## Learner's answer
# {inputs.user_answer}

# ## Rubric
# {format_rubric(criteria)}

# ## Instructions
# 1. For each rubric criterion, reason through whether the learner's answer satisfies it.
# 2. Assign points: full points if satisfied, 0 if not. No partial credit unless the criterion explicitly allows it.
# 3. Return your response as a JSON object in exactly this format, with no other text:

# {{
#   "criteria": [
#     {{ "label": "...", "satisfied": true, "points_awarded": 1, "reasoning": "..." }}
#   ],
#   "total_score": 0,
#   "max_score": {max_score},
#   "summary": "One or two sentence plain-language summary for the learner."
# }}"""
