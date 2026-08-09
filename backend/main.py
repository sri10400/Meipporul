from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
from evaluator import (
    evaluate_answer,
    generate_final_feedback
)


app = FastAPI(title="IntervueAI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

    # ==========================================
    # BASIC REQUEST VALIDATION
    # ==========================================

    session_id = request.sessionId.strip()

    if not session_id:
        raise HTTPException(
            status_code=400,
            detail="sessionId is required."
        )

    session = session_manager.get_session(session_id)

    # ==========================================
    # START NEW INTERVIEW
    # ==========================================

    if session is None:

        if request.candidate is None:
            raise HTTPException(
                status_code=400,
                detail="Candidate information is required to start the interview."
            )

        try:
            profile = build_candidate_profile(request.candidate)

            session = session_manager.create_session(
                session_id=session_id,
                candidate=request.candidate,
                profile=profile
            )

            # Create personalized interview plan
            plan = create_interview_plan(profile)

            session.interview_plan = plan

        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to create interview plan: {str(error)}"
            )

        if not plan:
            session.done = True

            return {
                "reply": "Unable to create an interview plan for this candidate.",
                "done": True
            }

        # Generate first question
        first_item = plan[0]

        day_data = get_day(first_item["day"])

        if day_data is None:
            raise HTTPException(
                status_code=500,
                detail=f"Curriculum information not found for day {first_item['day']}."
            )

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
    # PREVENT CONTINUING A COMPLETED INTERVIEW
    # ==========================================

    if session.done:
        return {
            "reply": "This interview has already been completed.",
            "done": True,
            "feedback": generate_final_feedback(session)
        }

    # ==========================================
    # ANSWER VALIDATION
    # ==========================================

    if request.message is None:
        return {
            "reply": "Please provide your answer.",
            "done": False
        }

    answer = request.message.strip()

    if not answer:
        return {
            "reply": "Your answer cannot be empty. Please provide a response.",
            "done": False
        }

    # ==========================================
    # SAVE CANDIDATE ANSWER
    # ==========================================

    session.answers.append(answer)

    # ==========================================
    # FIND CURRENT PLAN ITEM
    # ==========================================

    current_index = session.current_plan_index

    if current_index >= len(session.interview_plan):

        session.done = True

        feedback = generate_final_feedback(session)

        return {
            "reply": "Interview completed.",
            "done": True,
            "feedback": feedback
        }

    current_item = session.interview_plan[current_index]

    day_data = get_day(current_item["day"])

    if day_data is None:
        raise HTTPException(
            status_code=500,
            detail=f"Curriculum information not found for day {current_item['day']}."
        )

    objectives = day_data.get("objectives", [])

    if not objectives:
        raise HTTPException(
            status_code=500,
            detail=f"No learning objectives found for day {current_item['day']}."
        )

    objective = objectives[0]

    # ==========================================
    # EVALUATE ANSWER
    # ==========================================

    evaluation = evaluate_answer(
        answer,
        session.current_question,
        objective
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
            objective
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

    # ==========================================
    # CHECK INTERVIEW COMPLETION
    # ==========================================

    if session.current_plan_index >= len(session.interview_plan):

        session.done = True

        feedback = generate_final_feedback(session)

        return {
            "reply": "Interview completed.",
            "done": True,
            "feedback": feedback
        }

    # ==========================================
    # GENERATE NEXT QUESTION
    # ==========================================

    next_item = session.interview_plan[
        session.current_plan_index
    ]

    next_day_data = get_day(next_item["day"])

    if next_day_data is None:
        raise HTTPException(
            status_code=500,
            detail=f"Curriculum information not found for day {next_item['day']}."
        )

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