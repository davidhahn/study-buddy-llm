from src.types import ExerciseType, Language, Criterion

BASE_RUBRIC: list[Criterion] = [
    {
        "label": "Correct output",
        "points": 3,
        "description": "Produces the right result for the primary use case described in the problem. Before flagging a logical error, construct a concrete input example that demonstrates the failure. If you cannot construct a specific failing input, do not flag it as a logical error.",
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
            "description": "O(2n) and O(n) are the same complexity class. Constants are dropped in Big-O notation. Only flag if the complexity class itself differs (e.g. O(n^2) vs O(n)).",
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
