# study-buddy-llm

A personal AI-powered study system built in Python. It generates interview-caliber coding problems, grades submitted solutions against a structured rubric, and tracks performance over time to drive spaced repetition.

Built to solve a real problem — daily technical practice sessions were almost entirely manual. This replaces the overhead with an automated loop: generate problem → work on it → submit → get graded feedback → repeat, with the system learning what to resurface based on actual performance.

## Why This Exists

Most study tools are generic. The combination I needed — personalized generation, structured evaluation against a senior engineer rubric, and spaced repetition driven by real session data — didn't exist off the shelf.

Building it also forced hands-on work across every skill category that shows up in applied AI engineering roles: prompt engineering, eval framework design, LLM-as-judge reliability, structured output, and multi-component Python system design.

## Architecture

```
study-buddy-llm/
├── main.py              # CLI entry point
├── src/
│   ├── generator/       # Problem generation (Phase 1)
│   │   └── problem.py
│   └── grader/          # LLM-as-judge evaluation (Phase 2)
│       └── grade.py
├── db/                  # Schema and migrations (Phase 3+)
└── requirements.txt
```

### Phase 1 — Problem Generation ✅
Generates structured, interview-caliber problems given a topic and difficulty. Output includes a problem statement, constraints, examples, and optional setup code. Built with prompt iteration to produce problems specific enough to start immediately — not vague prompts like "build a dropdown."

### Phase 2 — Grading + Feedback ✅
Evaluates a submitted solution against a dual-track rubric:

**Quantitative:** correctness, edge case coverage, complexity

**Qualitative:** naming clarity, modularity, no dead code, single responsibility

Uses a two-pass evaluation approach with different framings (strengths vs. gaps) to reduce LLM-as-judge reliability issues — verbosity bias, position bias, self-preference bias, and sycophancy. The gaps framing is dominant; a >5% score discrepancy between passes flags the result as uncertain.

Rubric criteria support `cascading` evaluation dependencies — edge case handling, for example, is only evaluated when the primary output is correct.

### Phase 3 — Progress Tracking ✅
SQLite-based session logger. Stores per-session scores, rubric results, and timestamps. Queryable history for identifying patterns in what's being missed.

### Phase 4–6 — Spaced Repetition, Topic Suggestion, Schedule Generation 📋 Planned
SM-2 algorithm for scheduling problem reviews. Pattern analysis over session history for topic suggestions. Daily schedule generation that combines due reviews, weak topics, and available time.

## Eval Design

The hardest design problem in this system is preventing the model from grading its own output leniently. The grading component uses:

- **Rubric decomposition** — atomic yes/no criteria with specific descriptions, not holistic judgment
- **Two-pass evaluation** — strengths framing and gaps framing averaged with the gaps framing dominant
- **Chain-of-thought before verdict** — the model reasons through each criterion before scoring
- **Cascading dependencies** — criteria that depend on other criteria being satisfied first
- **Explicit complexity guidance** — criterion descriptions include concrete rules (e.g., "O(n) and O(2n) are the same complexity class")

## Stack

- **Python 3.14+**
- **Anthropic SDK** — Claude claude-sonnet-4-6 for generation and grading
- **SQLite** (Phase 3) → PostgreSQL migration planned
- CLI-first; no UI yet

## Getting Started

### Prerequisites
- Python 3.11+
- Anthropic API key

### Setup

```bash
git clone https://github.com/davidhahn/study-buddy-llm.git
cd study-buddy-llm

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```
ANTHROPIC_API_KEY=your_key_here
```

Run:

```bash
python main.py
```
