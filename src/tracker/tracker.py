from src.types import QuestionResponse, CriterionEvaluationResponse, Criterion
from src.grader.grader import calculate_sm2_score, calculate_initial_sm2_score
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()


def log_session(
    problem_id: int,
    answer: str,
    rubric: list[Criterion],
    evaluation_response: CriterionEvaluationResponse,
) -> int:
    db_path = os.environ.get("DB_PATH", "")
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.execute(
        "INSERT INTO sessions (total_score, max_score, is_uncertain, summary, answer) VALUES (?, ?, ?, ?, ?)",
        (
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
    is_correct_submission = False
    total_secondary_score = 0
    max_secondary_score = 0

    for criterion in evaluation_response["criteria"]:
        if criterion["id"] == "correct_output" and criterion["points_awarded"] != 0:
            is_correct_submission = True

        if (
            criterion["id"] != "correct_output"
            and rubric_lookup[criterion["id"]].get("evaluation_dependency")
            != "correct_output"
        ):
            max_secondary_score += rubric_lookup[criterion["id"]]["points"]
            total_secondary_score += criterion["points_awarded"]

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
    problem_cursor = connection.execute(
        "SELECT * FROM problems WHERE ID = (?)", (problem_id,)
    )
    problem = problem_cursor.fetchone()

    if problem is None:
        raise RuntimeError("Failed to fetch problem")

    ease_factor = problem["ease_factor"] if problem["ease_factor"] is not None else 2.5
    repetitions = problem["repetitions"] if problem["repetitions"] is not None else 0
    interval = problem["interval"] if problem["interval"] is not None else 0

    sm2_score = calculate_initial_sm2_score(
        is_correct_submission,
        evaluation_response["is_uncertain"],
        total_secondary_score,
        max_secondary_score,
    )
    updated_problem_values = calculate_sm2_score(
        {
            "sm2_score": sm2_score,
            "interval": interval,
            "repetitions": repetitions,
            "ease_factor": ease_factor,
        }
    )

    connection.execute(
        "UPDATE problems SET interval = ?, repetitions = ?, ease_factor = ?, next_review_date = ? WHERE id = ?",
        (
            updated_problem_values["interval"],
            updated_problem_values["repetitions"],
            updated_problem_values["ease_factor"],
            datetime.today() + timedelta(days=updated_problem_values["interval"]),
            problem_id,
        ),
    )
    connection.commit()
    connection.close()

    return session_id
