from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any

from candidate_profiler import build_candidate_profile
from session_manager import SessionManager


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

    # Start a new interview
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

        session.current_question = (
            "Tell me about your experience with AI engineering."
        )

        session.questions.append(session.current_question)
        session.question_count = 1

        return {
            "reply": session.current_question,
            "done": False
        }

    # Continue existing interview
    if request.message is not None:

        session.answers.append(request.message)

        session.current_question = (
            "Thank you. Can you explain one of the AI systems you have worked with?"
        )

        session.questions.append(session.current_question)
        session.question_count += 1

        return {
            "reply": session.current_question,
            "done": False
        }

    return {
        "reply": "Please provide your answer.",
        "done": False
    }