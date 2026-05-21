from src.generator.problem import generate_problem, Topic
from src.grader.rubric import build_rubric, ExerciseType, Language
from src.types import Difficulty
from src.grader.grader import grade_solution
import time

problem = generate_problem(Topic.BINARY_SEARCH_TREE, Difficulty.MEDIUM)
print("Problem generated")
print(problem)
print("-----------------")

rubric = build_rubric(ExerciseType.ALGORITHM, Language.JAVASCRIPT)
print("Rubric generated")
print(rubric)
print("-----------------")


answer = f"""function bst() {{
  console.log('solved. this answer should work!');
}}
"""
graded_solution = grade_solution(problem, answer, rubric)
print(graded_solution)
