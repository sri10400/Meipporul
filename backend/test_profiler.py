import json

from candidate_profiler import build_candidate_profile
from interview_engine import create_interview_plan
from curriculum_loader import get_day
from question_engine import generate_question
from evaluator import evaluate_answer


with open("../data/candidates.json", "r", encoding="utf-8") as file:
    data = json.load(file)


candidate = data["candidates"][0]

profile = build_candidate_profile(candidate)

plan = create_interview_plan(profile)


print("\nINTERVIEW PLAN\n")

for index, item in enumerate(plan, start=1):

    print(
        f"Q{index} | "
        f"Day {item['day']} | "
        f"{item['title']} | "
        f"Attempts: {item['attempts']}"
    )

    day_data = get_day(item["day"])

    if day_data:
        question = generate_question(
            day_data,
            question_number=index
        )

        print(f"Question: {question['question']}")
        print(f"Objective: {question['objective']}")

    print()


print("Total questions:", len(plan))
print("\nANSWER EVALUATION\n")

question = plan[0]

day_data = get_day(question["day"])

generated_question = generate_question(
    day_data,
    question_number=1
)

answer = (
    "Embeddings convert text into numerical vector representations "
    "that capture semantic meaning. Similar concepts are represented "
    "by vectors that are close together, which allows a vector database "
    "to perform semantic retrieval."
)

evaluation = evaluate_answer(
    answer,
    generated_question["question"],
    generated_question["objective"]
)

print("Question:")
print(generated_question["question"])

print("\nCandidate Answer:")
print(answer)

print("\nEvaluation:")
print(evaluation)