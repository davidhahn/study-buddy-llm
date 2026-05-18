from src.generator.problem import generate_problem, Topic
from src.grader.rubric import build_rubric, ExerciseType, Language

# print(generate_problem(Topic.BINARY_SEARCH_TREE, "medium"))
print(len(build_rubric(ExerciseType.ALGORITHM, Language.JAVASCRIPT)))
