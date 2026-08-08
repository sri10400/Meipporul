import json

from candidate_profiler import build_candidate_profile
from interview_engine import create_interview_plan
from curriculum_loader import get_day
from question_engine import generate_question


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