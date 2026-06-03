from src.types import QuestionResponse, CriterionEvaluationResponse, Criterion
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()


def log_session(
    question: QuestionResponse,
    answer: str,
    rubric: list[Criterion],
    evaluation_response: CriterionEvaluationResponse,
) -> int:
    """
    takes in question, answer, and the evaluation_response and create DB rows
    the return response is the session id that was created
    """
    db_path = os.environ.get("DB_PATH", "")
    connection = sqlite3.connect(db_path)
    cursor = connection.execute(
        "INSERT INTO sessions (topic, difficulty, exercise_type, language, total_score, max_score, is_uncertain, summary, answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            question["topic"],
            question["difficulty"],
            question["exercise_type"],
            question["language"],
            evaluation_response["total_score"],
            evaluation_response["max_score"],
            evaluation_response["is_uncertain"],
            answer,
            evaluation_response["summary"],
        ),
    )
    session_id = cursor.lastrowid

    if session_id is None:
        raise RuntimeError("Failed to create session row")

    rubric_lookup = {item["id"]: item for item in rubric}

    for criterion in evaluation_response["criteria"]:
        if not criterion["is_satisfied"]:
            connection.execute(
                "INSERT INTO failed_criteria (session_id, criterion_id, label, points_possible, reasoning) VALUES (?, ?, ?, ?, ?)",
                (
                    session_id,
                    criterion["id"],
                    criterion["label"],
                    rubric_lookup[criterion["id"]]["points"],
                    criterion["reasoning"],
                ),
            )
    connection.commit()
    connection.close()

    return session_id
