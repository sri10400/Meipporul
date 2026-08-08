from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any

app = FastAPI(title="IntervueAI")


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

    if request.candidate is not None and request.message is None:
        return {
            "reply": "Welcome to your AI Engineering interview. Let's begin.",
            "done": False
        }

    if request.message is not None:
        return {
            "reply": "Thank you. Let's continue with the next question.",
            "done": False
        }

    return {
        "reply": "Invalid interview request.",
        "done": False
    }