from typing import TypedDict
from enum import Enum
from src.types import Criterion, QuestionResponse
import os
from anthropic import Anthropic
import json
from dotenv import load_dotenv
import httpx


class Framing(str, Enum):
    STRENGTH = "strength"
    GAPS = "gaps"


class EvaluatedCriterion(TypedDict):
    label: str
    is_satisfied: bool
    points_awarded: int
    reasoning: str


class ClaudeEvaluationResponse(TypedDict):
    criteria: list[EvaluatedCriterion]
    total_score: float
    max_score: int
    summary: str


class CriterionEvaluationResponse(ClaudeEvaluationResponse):
    is_uncertain: bool


load_dotenv()
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    timeout=30.0,
    http_client=httpx.Client(limits=httpx.Limits(max_keepalive_connections=0)),
)


def grade_solution(
    question: QuestionResponse, answer: str, rubric: list[Criterion]
) -> CriterionEvaluationResponse:
    strength_prompt = build_judge_prompt(question, answer, rubric, Framing["STRENGTH"])
    gaps_prompt = build_judge_prompt(question, answer, rubric, Framing["GAPS"])

    print(f"Prompt length: {len(strength_prompt)} characters")

    strength_message = client.messages.create(
        max_tokens=4096,
        messages=[{"role": "user", "content": strength_prompt}],
        model="claude-sonnet-4-20250514",
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

    gaps_message = client.messages.create(
        max_tokens=4096,
        messages=[{"role": "user", "content": gaps_prompt}],
        model="claude-sonnet-4-20250514",
    )
    gaps_response_text = gaps_message.content[0].text
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
        f"{i + 1}. {criterion["label"]} ({criterion["points"]} pt): {criterion["description"]}"
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
1. For each rubric criterion, reason through whether the learner's answer satisfies it.
2. Assign points: full points if satisfied, 0 if not. No partial credit unless the criterion explicitly allows it.
3. Return your response as a JSON object in exactly this format, with no other text:

{{
    "criteria": [
        {{ "label": "...", "is_satisfied": true, "points_awarded": 1, "reasoning": "..." }}
    ],
    "total_score": 0,
    "max_score": {calculate_max_score(rubric)},
    "summary": "One or two sentence plain-language summary for the learner."
}}"""
