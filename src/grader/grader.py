from typing import TypedDict
from enum import Enum
from src.types import (
    Criterion,
    QuestionResponse,
    CriterionEvaluationResponse,
)
from src.client import anthropic_client
import json


class SM2Score(TypedDict):
    interval: int
    ease_factor: float
    repetitions: int
    sm2_score: int


class Framing(str, Enum):
    STRENGTH = "strength"
    GAPS = "gaps"


def grade_solution(
    question: QuestionResponse, answer: str, rubric: list[Criterion]
) -> CriterionEvaluationResponse:
    strength_prompt = build_judge_prompt(question, answer, rubric, Framing["STRENGTH"])
    gaps_prompt = build_judge_prompt(question, answer, rubric, Framing["GAPS"])

    print(f"Prompt length: {len(strength_prompt)} characters")

    strength_message = anthropic_client.messages.create(
        max_tokens=4096,
        messages=[{"role": "user", "content": strength_prompt}],
        model="claude-opus-4-6",
    )
    strength_response_text = strength_message.content[0].text
    strength_cleaned = (
        strength_response_text.strip()
        .removeprefix("```json")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )
    strength_json = json.loads(strength_cleaned)

    gaps_message = anthropic_client.messages.create(
        max_tokens=4096,
        messages=[{"role": "user", "content": gaps_prompt}],
        model="claude-opus-4-6",
    )
    gaps_response_text = gaps_message.content[0].text
    print("gaps_response_text")
    print(gaps_response_text)
    gaps_cleaned = (
        gaps_response_text.strip()
        .removeprefix("```json")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )
    gaps_json = json.loads(gaps_cleaned)
    result: CriterionEvaluationResponse = {
        "criteria": [],
        "total_score": 0,
        "max_score": 0,
        "summary": "",
        "is_uncertain": False,
    }
    max_strengths_score = 0
    max_gaps_score = 0

    for strength_criterion, gaps_criterion in zip(
        strength_json["criteria"], gaps_json["criteria"]
    ):
        is_satisfied = (
            strength_criterion["is_satisfied"] and gaps_criterion["is_satisfied"]
        )
        strengths_score = strength_criterion["points_awarded"]
        gaps_score = gaps_criterion["points_awarded"]

        result["criteria"].append(
            {
                "id": gaps_criterion["id"],
                "label": gaps_criterion["label"],
                "is_satisfied": is_satisfied,
                "points_awarded": round((strengths_score + gaps_score) / 2),
                "reasoning": gaps_criterion["reasoning"],
            }
        )

        max_strengths_score += strengths_score
        max_gaps_score += gaps_score

    avg_score = (max_strengths_score + max_gaps_score) / 2
    score_diff_percentage = abs(max_strengths_score - max_gaps_score) / avg_score * 100

    result["total_score"] = sum(
        criterion["points_awarded"] for criterion in result["criteria"]
    )
    result["max_score"] = calculate_max_score(rubric)
    result["is_uncertain"] = True if score_diff_percentage > 5 else False
    result["summary"] = gaps_json["summary"]

    return result


def format_rubric(rubric: list[Criterion]) -> str:
    return "\n".join(
        f"{i + 1}. [{criterion['id']}] {criterion['label']} ({criterion['points']} pt): {criterion['description']}"
        + (
            f" Depends on criterion: '{criterion['evaluation_dependency']}'."
            if criterion.get("evaluation_dependency")
            else ""
        )
        for i, criterion in enumerate(rubric)
    )


def calculate_max_score(rubric: list[Criterion]) -> int:
    return sum(criterion["points"] for criterion in rubric)


def build_judge_prompt(
    question: QuestionResponse, answer: str, rubric: list[Criterion], framing: Framing
) -> str:

    return f"""You are an objective evaluator for a coding study application. \
Your job is to assess a learner's answer against a reference answer using a specific rubric.

Do not be lenient. Do not reward effort or length. Evaluate only what is stated in the rubric.
{"Focus on what the learner is doing well." if framing == Framing["STRENGTH"] else "Focus on what the learner is missing or could fail"}

## Question
{question["prompt"]}

## Learner's answer
{answer}

## Rubric
{format_rubric(rubric)}

## Instructions
1. Do not output any text before or after the JSON object. All reasoning must be inside the reasoning field of each criterion.
2. For each rubric criterion, reason through whether the learner's answer satisfies it.
3. The "id" field must exactly match the criterion id from the rubric as shown in brackets e.g. [correct_output]
4. The "label" field must exactly match the label from the rubric
5. The "is_satisfied" field must be true only if the criterion is fully met, false otherwise. For criteria that depend on another criterion (cascading), if the dependency failed, it must be false regardless of the solution quality.
6. The "points_awarded" field must have full points if satisfied, 0 if not. No partial credit unless the criterion explicitly allows it.
7. The "reasoning" field must give a short concise reason for why it was given for the evaluation
8. The "total_score" field must add up "points_awarded" from the criteria.
9. The "summary" field should provide one or two sentence plain-language summary for the learner.
10. Return your response as the following JSON object in exactly this format, with no other text:

{{
    "criteria": [
        {{ "id": "criterion_id_from_rubric", "label": "...", "is_satisfied": true, "points_awarded": 1, "reasoning": "..." }}
    ],
    "total_score": 0,
    "max_score": {calculate_max_score(rubric)},
    "summary": "One or two sentence plain-language summary for the learner."
}}"""


def calculate_sm2_score(sm2_score_props: SM2Score) -> SM2Score:
    """
    if sm2_score is < 3 (i.e. failed)
        - repetitions resets to 0
        - interval resets to 1
        - ease_factor decreases

    if sm2_score is >= 3
        - repetitions increments by 1
        - interval is calculated based on repetitions
            - first review (repetitions = 1) -> interval = 1
            - second review (repetitions = 2) -> interval = 6
            - after that -> previous interval * ease_factor
        - ease_factor adjusts based on score -> formula: ease_factor + (0.1 - (5 - sm2_score) * 0.08)
    """
    sm2_score = sm2_score_props["sm2_score"]
    ease_factor = sm2_score_props["ease_factor"]
    repetitions = sm2_score_props["repetitions"]
    interval = sm2_score_props["interval"]

    if sm2_score < 3:
        repetitions = 0
        interval = 1

    else:
        repetitions += 1
        if repetitions == 1:
            interval = 1
        elif repetitions == 2:
            interval = 6
        else:
            interval = round(interval * ease_factor)

    ease_factor = ease_factor + (0.1 - (5 - sm2_score) * 0.08)
    if ease_factor <= 1.3:
        ease_factor = 1.3

    return {
        "repetitions": repetitions,
        "interval": interval,
        "ease_factor": ease_factor,
        "sm2_score": sm2_score,
    }
