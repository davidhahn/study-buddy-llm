import json
from src.types import (
    Topic,
    GeneratedProblem,
    Difficulty,
    ExerciseType,
    Language,
    ProblemRow,
)
from src.client import anthropic_client
from typing import cast
import os
import datetime
from dotenv import load_dotenv
import sqlite3

load_dotenv()


def generate_problem(
    exercise_type: ExerciseType,
    language: Language,
    topic: Topic,
    difficulty: Difficulty,
) -> GeneratedProblem:
    prompt = f"""Generate a {exercise_type} software engineering interview practice problem for the following in {language}:
    - Topic: {topic}
    - Difficulty: {difficulty}
    Focus on problems commonly asked in technical interviews at mid-size to large tech companies.

    Return only a JSON object with exactly these keys:
    {{
        "topic": "{topic.value}",
        "difficulty": "{difficulty.value}",
        "exercise_type": "{exercise_type.value}",
        "language": "{language.value}",
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
    try:
        question_response = json.loads(cleaned)
        db_path = os.environ.get("DB_PATH", "")
        with sqlite3.connect(db_path) as connection:
            cursor = connection.execute(
                "INSERT INTO problems (topic, difficulty, exercise_type, language, prompt, constraints, examples, setup_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    topic.value,
                    difficulty.value,
                    exercise_type.value,
                    language.value,
                    question_response["prompt"],
                    json.dumps(question_response["constraints"]),
                    json.dumps(question_response["examples"]),
                    question_response["setup_code"],
                ),
            )

            problem_id = cursor.lastrowid

            if problem_id is None:
                raise RuntimeError("Failed to create problem")

            return {"question": question_response, "problem_id": problem_id}

    except json.JSONDecodeError as error:
        raise error
    except TypeError:
        raise RuntimeError("Cleaned response is not a valid JSON string")


def get_due_problems(anchor_date: datetime.datetime) -> list[ProblemRow]:
    db_path = os.environ.get("DB_PATH", "")
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute(
            "SELECT * FROM problems WHERE next_review_date <= (?)", (anchor_date,)
        )

        problems = [cast(ProblemRow, dict(row)) for row in cursor.fetchall()]

        return problems
