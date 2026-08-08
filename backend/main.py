from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any

from candidate_profiler import build_candidate_profile
from session_manager import SessionManager
from interview_engine import (
    create_interview_plan,
    generate_follow_up
)
from curriculum_loader import get_day
from question_engine import generate_question
from evaluator import evaluate_answer


app = FastAPI(title="IntervueAI")

session_manager = SessionManager()


class InterviewRequest(BaseModel):
    sessionId: str
    candidate: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


@app.get("/")
def root():
    return {
        "message": "IntervueAI API is running"
    }


@app.post("/api/interview")
def interview(request: InterviewRequest):

    session = session_manager.get_session(request.sessionId)

    # ==========================================
    # START NEW INTERVIEW
    # ==========================================
    if session is None:

        if request.candidate is None:
            return {
                "reply": "Candidate information is required to start the interview.",
                "done": False
            }

        profile = build_candidate_profile(request.candidate)

        session = session_manager.create_session(
            session_id=request.sessionId,
            candidate=request.candidate,
            profile=profile
        )

        # Create personalized interview plan
        plan = create_interview_plan(profile)

        session.interview_plan = plan

        if not plan:
            session.done = True

            return {
                "reply": "Unable to create an interview plan for this candidate.",
                "done": True
            }

        # Generate first question
        first_item = plan[0]

        day_data = get_day(first_item["day"])

        question_data = generate_question(
            day_data,
            question_number=1
        )

        session.current_question = question_data["question"]
        session.questions.append(question_data["question"])
        session.question_count = 1

        session.topics_covered.append(first_item["day"])

        return {
            "reply": question_data["question"],
            "done": False
        }

    # ==========================================
    # CONTINUE EXISTING INTERVIEW
    # ==========================================
    if request.message is None:
        return {
            "reply": "Please provide your answer.",
            "done": False
        }

    # Save candidate answer
    session.answers.append(request.message)

    # Find current plan item
    current_index = session.current_plan_index

    if current_index >= len(session.interview_plan):
        session.done = True

        return {
            "reply": "Interview completed.",
            "done": True
        }

    current_item = session.interview_plan[current_index]

    day_data = get_day(current_item["day"])

    if day_data is None:
        return {
            "reply": "Curriculum information could not be found.",
            "done": False
        }

    # Evaluate answer
    evaluation = evaluate_answer(
        request.message,
        session.current_question,
        day_data.get("objectives", [""])
    )

    # Store score
    session.scores[current_item["day"]] = evaluation

    # ==========================================
    # ADAPTIVE FOLLOW-UP
    # ==========================================
    if (
        evaluation.get("follow_up_needed")
        and not session.follow_up_used
    ):

        follow_up = generate_follow_up(
            evaluation,
            session.current_question,
            day_data.get("objectives", [""])[0]
        )

        session.current_question = follow_up
        session.questions.append(follow_up)
        session.question_count += 1

        session.follow_up_used = True

        return {
            "reply": follow_up,
            "done": False
        }

    # ==========================================
    # MOVE TO NEXT PLANNED TOPIC
    # ==========================================

    session.follow_up_used = False
    session.current_plan_index += 1

    # Check whether interview is finished
    if session.current_plan_index >= len(session.interview_plan):

        session.done = True

        return {
            "reply": "Interview completed. Your feedback is being prepared.",
            "done": True
        }

    next_item = session.interview_plan[
        session.current_plan_index
    ]

    next_day_data = get_day(next_item["day"])

    next_question = generate_question(
        next_day_data,
        question_number=session.question_count + 1
    )

    session.current_question = next_question["question"]
    session.questions.append(next_question["question"])
    session.question_count += 1

    session.topics_covered.append(next_item["day"])

    return {
        "reply": next_question["question"],
        "done": False
    }