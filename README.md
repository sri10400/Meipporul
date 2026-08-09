# IntervueAI

IntervueAI is an adaptive AI-powered technical interview system designed to evaluate a candidate's technical understanding through a conversational interview.

The system uses a candidate's synthetic learning journey and completed curriculum missions to create a personalized interview plan. During the interview, candidate responses are evaluated and follow-up questions are generated when additional clarification or deeper understanding is required.

## Features

- Conversational technical interview
- Personalized interview plan based on candidate learning history
- Minimum 8 technical questions
- Coverage across multiple curriculum days
- Adaptive follow-up questions
- Candidate response evaluation
- Session-based conversation context
- Structured final feedback
- Overall technical score
- Strengths identification
- Areas for improvement
- Recommended next steps
- Responsive React-based interview interface

## Architecture

```text
React Frontend
      |
      | HTTP POST
      v
FastAPI Backend
      |
      +-- Candidate Profiler
      |
      +-- Interview Engine
      |
      +-- Question Engine
      |
      +-- Session Manager
      |
      +-- Answer Evaluator
      |
      v
Structured Interview Feedback
      |
      v
React Results Screen

Interview Flow
Candidate Profile
       |
       v
Build Candidate Profile
       |
       v
Create Interview Plan
       |
       v
Generate Question
       |
       v
Candidate Answer
       |
       v
Evaluate Answer
       |
       +---- Follow-up required ----+
       |                            |
       |                            v
       |                     Generate Follow-up
       |                            |
       +------------+---------------+
                    |
                    v
              Next Question
                    |
                    v
          Interview Completed
                    |
                    v
          Generate Final Feedback
Technology Stack
Frontend
React
Vite
JavaScript
CSS
Backend
Python
FastAPI
Pydantic
Uvicorn
Project Structure
Meipporul/
│
├── backend/
│   ├── main.py
│   ├── candidate_profiler.py
│   ├── session_manager.py
│   ├── interview_engine.py
│   ├── question_engine.py
│   ├── curriculum_loader.py
│   ├── evaluator.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── services/
│   │       └── interviewApi.js
│   ├── package.json
│   └── vite.config.js
│
├── data/
│
├── PROMPTS.md
├── README.md
└── .gitignore
API
POST /api/interview

The main interview endpoint is used for both starting an interview and submitting candidate answers.

Start Interview

The frontend sends a candidate profile and session ID to the endpoint.

Example:

{
  "sessionId": "test-session-001",
  "candidate": {
    "member": {
      "id": "candidate-001",
      "name": "Emily Chen",
      "jobRole": "AI Engineer",
      "yearsExperience": 6,
      "education": "Computer Science",
      "status": "active"
    },
    "missions": [
      {
        "day": 1,
        "title": "Embeddings Explained",
        "passed": true,
        "attempts": 1
      }
    ],
    "signals": {
      "commitDays": 31,
      "missionsCompleted": 8,
      "missionsFirstTry": 4
    }
  }
}

Example response:

{
  "reply": "Interview question...",
  "done": false
}
Submit Answer

Example:

{
  "sessionId": "test-session-001",
  "message": "Candidate's technical answer..."
}

The backend returns either the next question, an adaptive follow-up question, or the final feedback.

Final Response
{
  "reply": "Interview completed.",
  "done": true,
  "feedback": {
    "overall_score": 75,
    "performance": "Good foundation with some areas to strengthen.",
    "strengths": [],
    "areas_to_improve": [],
    "recommendation": "Review weaker concepts and practice explaining technical decisions in greater depth."
  }
}
Minimum Requirements Coverage
Requirement	Implementation
Conversational technical interview	React interview interface with FastAPI communication
Minimum 8 questions	Interview plan creates a minimum of 8 questions
At least 4 curriculum days	Questions are selected from different completed curriculum days
Follow-up questions	Evaluator determines when an adaptive follow-up is required
Conversation context	SessionManager maintains interview state and responses
Structured feedback	Final evaluator returns score, performance, strengths, improvement areas and recommendation
Required HTTP endpoint	POST /api/interview
Running Locally
Backend
cd backend
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload

Backend:

http://127.0.0.1:8000
Frontend

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173
Scope

The project uses synthetic candidate and curriculum data provided for the hackathon challenge.

The implementation focuses on the adaptive technical interview experience. Authentication, persistent user accounts, voice interaction, mobile applications, and long-term conversation history are outside the required scope.

Team

Built as a hackathon project focused on adaptive technical interviewing and AI-assisted development.

License

This project was created for hackathon evaluation using synthetic challenge data.