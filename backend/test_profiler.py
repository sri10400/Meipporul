import json

from candidate_profiler import build_candidate_profile
from interview_engine import create_interview_plan
from curriculum_loader import get_day
from question_engine import generate_question
from evaluator import evaluate_answer
from interview_engine import generate_follow_up
from evaluator import generate_final_feedback


with open("../data/candidates.json", "r", encoding="utf-8") as file:
    data = json.load(file)


candidate = data["candidates"][0]

profile = build_candidate_profile(candidate)

plan = create_interview_plan(profile)

print("\nFINAL FEEDBACK TEST\n")


class MockSession:
    def __init__(self):
        self.scores = {
            7: {
                "score": 4,
                "level": "strong",
                "reason": "Strong understanding of embeddings."
            },
            8: {
                "score": 3,
                "level": "partial",
                "reason": "Good understanding of vector databases but needs more depth."
            },
            10: {
                "score": 4,
                "level": "strong",
                "reason": "Strong understanding of retrieval systems."
            },
            16: {
                "score": 3,
                "level": "partial",
                "reason": "Understands API integration but needs more architectural detail."
            }
        }


mock_session = MockSession()

feedback = generate_final_feedback(mock_session)

print(feedback)