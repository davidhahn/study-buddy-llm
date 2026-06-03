import json
from src.types import Topic, QuestionResponse, Difficulty, ExerciseType, Language
from src.client import anthropic_client


def generate_problem(
    exercise_type: ExerciseType,
    language: Language,
    topic: Topic,
    difficulty: Difficulty,
) -> QuestionResponse:
    prompt = f"""Generate a {exercise_type} software engineering interview practice problem for the following in {language}:
    - Topic: {topic}
    - Difficulty: {difficulty}
    Focus on problems commonly asked in technical interviews at mid-size to large tech companies.

    Return only a JSON object with exactly these keys:
    {{
        "topic": "{topic}",
        "difficulty": "{difficulty}",
        "exercise_type": "{exercise_type}",
        "language": "{language}",
        "prompt": "...",
        "constraints": [],
        "examples": [],
        "setup_code": "..."
    }}

    prompt: clear explanation of the problem
    constraints: list of specific requirements the solution must meet
    examples: list of input/output pairs
    setup_code: string containing boilerplate code, or null if not needed
    Do not wrap the response in markdown code blocks. Return raw JSON only.
    """

    message = anthropic_client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        model="claude-opus-4-6",
    )

    response_text = message.content[0].text
    cleaned = (
        response_text.strip()
        .removeprefix("```json")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )
    return json.loads(cleaned)
