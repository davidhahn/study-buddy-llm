from src.generator.problem import generate_problem, Topic
from src.grader.rubric import build_rubric, ExerciseType, Language
from src.types import Difficulty, QuestionResponse
from src.grader.grader import grade_solution
from src.util.mock import binary_tree_problem, binary_tree_answer
from typing import cast
import time

# problem = generate_problem(Topic.BINARY_SEARCH_TREE, Difficulty.MEDIUM)
problem = cast(QuestionResponse, binary_tree_problem)
print("Problem generated")
print(problem)
print("-----------------")

rubric = build_rubric(ExerciseType.ALGORITHM, Language.JAVASCRIPT)
print("Rubric generated")
print(rubric)
print("-----------------")


answer = binary_tree_answer
graded_solution = grade_solution(problem, answer, rubric)
print(graded_solution)
