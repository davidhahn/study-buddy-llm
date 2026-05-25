from src.types import ExerciseType, Language, Criterion

BASE_RUBRIC: list[Criterion] = [
    {
        "id": "correct_output",
        "label": "Correct output",
        "points": 3,
        "evaluation_type": "independent",
        "description": "Produces the right result for the primary use case described in the problem. Before flagging a logical error, construct a concrete input example that demonstrates the failure. If you cannot construct a specific failing input, do not flag it as a logical error.",
    },
    {
        "id": "edge_cases_handled",
        "label": "Edge cases handled",
        "points": 2,
        "evaluation_type": "cascading",
        "evaluation_dependency": "correct_output",
        "description": "Handles empty input, null/None, zero, or boundary values without crashing or returning wrong output.",
    },
    {
        "id": "clear_naming",
        "label": "Clear naming",
        "points": 1,
        "evaluation_type": "independent",
        "description": "Variable and function names describe what they hold or do. Single-letter names only acceptable as loop counters in simple iterations.",
    },
    {
        "id": "no_unnecessary_nesting",
        "label": "No unnecessary nesting",
        "points": 1,
        "evaluation_type": "independent",
        "description": "Conditionals not nested more than 2 levels deep. Guard clauses used to handle invalid input early.",
    },
    {
        "id": "no_dead_code",
        "label": "No dead code",
        "points": 1,
        "evaluation_type": "independent",
        "description": "No unused variables, unreachable branches, or commented-out code blocks.",
    },
    {
        "id": "single_responsibility",
        "label": "Single responsibility",
        "points": 1,
        "evaluation_type": "independent",
        "description": "Each function does one describable thing. If a function needs 'and' to describe it, it should be split.",
    },
    {
        "id": "modular_extensible",
        "label": "Modular and extensible",
        "points": 2,
        "evaluation_type": "independent",
        "description": "Adding a related feature should not require rewriting existing logic — only adding to it.",
    },
    {
        "id": "no_unnecessary_complexity_overhead",
        "label": "No unnecessary complexity overhead",
        "points": 1,
        "evaluation_type": "independent",
        "description": "If a simpler approach has the same Big-O complexity, it is preferred. Only flag performance if a significantly better complexity class is straightforward.",
    },
]

EXERCISE_RUBRICS: dict[ExerciseType, list[Criterion]] = {
    ExerciseType.ALGORITHM: [
        {
            "id": "correct_time_complexity",
            "label": "Correct time complexity",
            "points": 2,
            "evaluation_type": "independent",
            "description": "O(2n) and O(n) are the same complexity class. Constants are dropped in Big-O notation. Only flag if the complexity class itself differs (e.g. O(n^2) vs O(n)).",
        },
        {
            "id": "correct_space_complexity",
            "label": "Correct space complexity",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Solution does not allocate unnecessary data structures. Auxiliary space is proportional to what the algorithm genuinely requires.",
        },
        {
            "id": "no_off_by_one_errors",
            "label": "No off-by-one errors",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Loop boundaries, array indices, and slice ranges are correct. Check start/end conditions explicitly.",
        },
        {
            "id": "terminates_correctly",
            "label": "Terminates correctly",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Recursive solutions have a clear base case. Iterative solutions cannot infinite-loop on valid input.",
        },
        {
            "id": "data_structure_choice_justified",
            "label": "Data structure choice is justified",
            "points": 1,
            "evaluation_type": "independent",
            "description": "The chosen data structure suits the access patterns of the problem.",
        },
    ],
    ExerciseType.UI_COMPONENT: [
        {
            "id": "props_input_minimal_typed",
            "label": "Props / inputs are minimal and typed",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Component accepts only what it needs. Props are clearly named and typed correctly.",
        },
        {
            "id": "state_is_local_where_possible",
            "label": "State is local where possible",
            "points": 1,
            "evaluation_type": "independent",
            "description": "State is not lifted higher than necessary. Only state that genuinely needs to be shared is elevated.",
        },
        {
            "id": "handles_loading_error_states",
            "label": "Handles loading and error states",
            "points": 2,
            "evaluation_type": "independent",
            "description": "Component renders meaningful loading and error states — not simply None or a blank render.",
        },
        {
            "id": "no_logic_in_render_return",
            "label": "No logic in the render / return",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Business logic and data transformation happen outside the template. The return block should be declarative.",
        },
        {
            "id": "accessible markup",
            "label": "Accessible markup",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Interactive elements use semantic HTML. Images have alt text. Form inputs have labels.",
        },
        {
            "id": "no_hardcoded_values_in_render",
            "label": "No hardcoded values in render",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Strings, colors, sizes, and magic numbers are not inline in the markup.",
        },
    ],
    ExerciseType.ASYNC: [
        {
            "id": "errors_caught_handled",
            "label": "Errors are caught and handled",
            "points": 2,
            "evaluation_type": "independent",
            "description": "All async operations are wrapped in try/except. Errors are not silently swallowed.",
        },
        {
            "id": "no_unhandled_exceptions",
            "label": "No unhandled exceptions in coroutines",
            "points": 2,
            "evaluation_type": "independent",
            "description": "Every awaitable that can raise is inside a try/except or has explicit error handling. Unawaited coroutines are not present.",
        },
        {
            "id": "no_unnecessary_sequential_awaits",
            "label": "No unnecessary sequential awaits",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Independent async operations run concurrently with asyncio.gather(). Sequential awaits only where one operation genuinely depends on the previous result.",
        },
        {
            "id": "loading_and_error_state_are_tracked",
            "label": "Loading and error state are tracked",
            "points": 1,
            "evaluation_type": "independent",
            "description": "The caller can determine whether the operation is in-flight, succeeded, or failed.",
        },
        {
            "id": "no_race_conditions",
            "label": "No race conditions",
            "points": 1,
            "evaluation_type": "independent",
            "description": "If concurrent tasks write shared state, appropriate locks or task-safe patterns are used.",
        },
    ],
}

LANGUAGE_RUBRICS: dict[Language, list[Criterion]] = {
    Language.JAVASCRIPT: [
        {
            "id": "correct_use_of_const_let",
            "label": "Correct use of const/let",
            "points": 1,
            "evaluation_type": "independent",
            "description": "No var. let only where reassignment actually occurs. const everywhere else.",
        },
        {
            "id": "no_input_mutation",
            "label": "No input mutation",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Functions do not modify arrays or objects passed as arguments unless mutation is explicitly the stated purpose.",
        },
        {
            "id": "destructuring_used_where_it_improves_clarity",
            "label": "Destructuring used where it improves clarity",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Object and array destructuring preferred over repeated property access where it aids readability.",
        },
        {
            "id": "no_implicit_type_coercion",
            "label": "No implicit type coercion",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Strict equality (===) used throughout. No reliance on truthy/falsy coercion where an explicit check is clearer.",
        },
    ],
    Language.PYTHON: [
        {
            "id": "follows_pep_8_naming_conventions",
            "label": "Follows PEP 8 naming conventions",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Variables and functions use snake_case. Classes use PascalCase. Constants use UPPER_SNAKE_CASE.",
        },
        {
            "id": "uses_pythonic_idioms_where_appropriate",
            "label": "Uses Pythonic idioms where appropriate",
            "points": 1,
            "evaluation_type": "independent",
            "description": "List comprehensions preferred over manual appends for simple cases. enumerate() over range(len()). zip() for parallel iteration.",
        },
        {
            "id": "no_bare_except_clauses",
            "label": "No bare except clauses",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Except clauses catch specific exception types. Bare except: or except Exception: without re-raising or logging is a flag.",
        },
        {
            "id": "type_hints_used_on_function_signatures",
            "label": "Type hints used on function signatures",
            "points": 1,
            "evaluation_type": "independent",
            "description": "Function parameters and return types are annotated. Internal variable hints are optional.",
        },
        {
            "id": "no_mutable_default_arguments",
            "label": "No mutable default arguments",
            "points": 1,
            "evaluation_type": "independent",
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
