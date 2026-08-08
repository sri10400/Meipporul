
import json

from candidate_profiler import build_candidate_profile
from interview_engine import create_interview_plan


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
        f"Attempts: {item['attempts']} | "
        f"Type: {item['type']}"
    )

print("\nTotal questions:", len(plan))