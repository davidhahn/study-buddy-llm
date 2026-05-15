import os
from anthropic import Anthropic
import json
from dotenv import load_dotenv


load_dotenv()
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def generate_problem(topic: str, difficulty: str) -> dict:
    prompt = f"""Generate a software engineering interview practice problem for the following:
    - Topic: {topic}
    - Difficulty: {difficulty}

    Return only a JSON object with exactly these keys:
    {{
      "topic": "{topic}",
      "difficulty": "{difficulty}",
      "prompt": "...",
      "constraints": [],
      "examples": []
    }}

    prompt: clear explanation of the problem
    constraints: list of specific requirements the solution must meet
    examples: list of input/output pairs
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
