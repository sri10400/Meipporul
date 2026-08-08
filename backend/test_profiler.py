import json
from candidate_profiler import build_candidate_profile


with open("../data/candidates.json", "r", encoding="utf-8") as file:
    data = json.load(file)


candidate = data["candidates"][0]

profile = build_candidate_profile(candidate)

print(json.dumps(profile, indent=2))