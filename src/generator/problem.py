import os
from anthropic import Anthropic
import json
from dotenv import load_dotenv
from enum import Enum

class Topic(str, Enum):
    PRACTICAL_PROBLEMS = "Practical Problems"
    BINARY_SEARCH_TREE = "Binary Search Tree"
    TREES = "Trees"
    TRIES = "Tries"
    GRAPHS = "Graphs"
    ARRAYS = "Arrays"
    STRINGS = "Strings"


load_dotenv()
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def generate_problem(topic: Topic, difficulty: str) -> dict:
    prompt = f"""Generate a software engineering interview practice problem for the following:
    - Topic: {topic}
    - Difficulty: {difficulty}
    Focus on problems commonly asked in technical interviews at mid-size to large tech companies.

    Return only a JSON object with exactly these keys:
    {{
      "topic": "{topic}",
      "difficulty": "{difficulty}",
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

    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="claude-sonnet-4-20250514"
    )

    response_text = message.content[0].text
    cleaned = response_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(cleaned)
