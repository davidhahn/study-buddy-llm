from src.types import QuestionResponse, CriterionEvaluationResponse


def log_session(
    question: QuestionResponse,
    answer: str,
    evaluation_response: CriterionEvaluationResponse,
) -> int:
    """
    takes in question, answer, and the evaluation_response and create DB rows
    the return response is the session id that was created
    """
