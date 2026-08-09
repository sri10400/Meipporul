# PROMPTS.md

# IntervueAI - AI-Assisted Development Log

This document records the AI-assisted development process used while building IntervueAI.

The project was developed iteratively by designing the architecture, implementing the frontend and backend separately, integrating the HTTP API, debugging the integration, and testing the complete adaptive interview flow.

---

## 1. Project Architecture

### Prompt

We have a hackathon project for an AI-powered adaptive technical interview. The system should conduct a conversational technical interview based on candidate learning history and curriculum data. Help us plan the project architecture and separate frontend and backend responsibilities.

### Development Outcome

The project was organized into:

- React/Vite frontend
- FastAPI backend
- Candidate profiling
- Interview planning
- Question generation
- Session management
- Answer evaluation
- Structured final feedback
- HTTP API integration

---

## 2. Git Branching

### Prompt

There are two branches: feature/frontend and feature/backend. The frontend and backend should be developed independently and integrated later. Explain how each team member should work on their branch and integrate the final project.

### Development Outcome

Frontend and backend were developed independently and later combined through an integration branch.

```text
feature/frontend
       \
        integration
       /
feature/backend

3. Frontend Development
Prompt

Create the frontend using React and Vite. We need a professional technical interview interface with a candidate introduction, interview coverage, question screen, answer area, progress indicator, adaptive interview experience, and final results screen.

Development Outcome

The React frontend was implemented with:

Candidate introduction
Interview coverage
Technical interview screen
Question counter
Interview journey
Answer textarea
Progress indicator
Evaluation state
Results screen
4. Backend API
Prompt

Build a FastAPI backend for an adaptive technical interview. The API should expose POST /api/interview and support starting an interview with candidate information and continuing an interview with candidate answers.

Development Outcome

The FastAPI backend exposes:

POST /api/interview

The endpoint supports:

Starting a new interview.
Submitting answers during an existing interview.
5. Candidate Profiling
Prompt

Build a candidate profile from synthetic candidate data containing member information, completed missions, failed or skipped missions, and learning signals. Use this profile to identify strengths, weak areas, and recommended interview difficulty.

Development Outcome

The candidate profiler processes:

Candidate information
Completed missions
Failed missions
Skipped missions
Learning signals
Strengths
Weak areas
Recommended difficulty
6. Interview Planning
Prompt

Create an interview plan from the candidate profile. The interview must contain at least 8 questions and should select different completed curriculum days first.

Development Outcome

The interview engine creates an interview plan with a minimum of 8 planned questions and prioritizes completed curriculum areas.

7. Adaptive Follow-Up Questions
Prompt

Add adaptive follow-up questions based on the evaluation of a candidate's previous answer. Strong, partial, and weak responses should receive different follow-up directions.

Development Outcome

The interview engine generates follow-up questions based on the evaluation level of the candidate's previous response.

The interview supports:

Strong response
      |
      v
Deeper technical follow-up

Partial response
      |
      v
Implementation-focused follow-up

Weak response
      |
      v
Simplified conceptual follow-up
8. Answer Evaluation
Prompt

Build an evaluator that analyzes a candidate's technical answer and determines a score, evaluation level, reason, and whether a follow-up question is needed.

Development Outcome

The evaluator produces structured evaluation information including:

Score
Evaluation level
Reason
Follow-up requirement
9. Structured Final Feedback
Prompt

Generate structured final feedback after the interview. The result should include an overall score, performance description, strengths, areas to improve, and a recommendation.

Development Outcome

The final feedback structure contains:

{
  "overall_score": 0,
  "performance": "",
  "strengths": [],
  "areas_to_improve": [],
  "recommendation": ""
}

The React results screen displays this backend-generated feedback.

10. Frontend API Integration
Prompt

Connect the React frontend to the FastAPI backend. Starting the interview should call the backend and display the returned question. Submitting an answer should call the same endpoint and display the returned next question or adaptive follow-up.

Development Outcome

A frontend API service was created:

frontend/src/services/interviewApi.js

It provides:

startInterview()
sendAnswer()

The React application communicates with:

POST /api/interview
11. Debugging the Frontend Flow
Prompt

The frontend appears to work using its own hardcoded questions and is not calling the backend. Check the interview start and submit functions and connect them to the API service.

Development Outcome

The local interview flow was replaced with backend-driven interaction.

The final flow became:

Start Interview
      |
      v
POST /api/interview
      |
      v
Backend Question
      |
      v
Candidate Answer
      |
      v
POST /api/interview
      |
      v
Evaluation
      |
      v
Follow-up / Next Question
12. CORS Debugging
Prompt

The frontend is sending OPTIONS /api/interview but FastAPI returns 405 Method Not Allowed. Configure FastAPI CORS correctly so the React development server can communicate with the API.

Development Outcome

FastAPI CORSMiddleware was configured for the local React development servers.

After the change, the backend successfully returned:

OPTIONS /api/interview 200 OK
POST /api/interview 200 OK

This confirmed successful frontend/backend communication.

13. Dynamic Results
Prompt

Replace the hardcoded interview score and feedback in the React results screen with the real feedback returned by the backend.

Development Outcome

The results screen was connected to:

feedback.overall_score
feedback.performance
feedback.strengths
feedback.areas_to_improve
feedback.recommendation

The results are now generated from the backend response instead of hardcoded scores.

14. Feedback Cleanup
Prompt

The backend is returning the same improvement message multiple times in the final feedback. Deduplicate the areas_to_improve list while preserving different feedback messages.

Development Outcome

The final feedback generation was updated so identical improvement messages are not repeated unnecessarily.

15. End-to-End Testing
Prompt

Verify whether the frontend and backend are actually integrated. Check the browser network requests and FastAPI logs and confirm that the interview requests reach POST /api/interview.

Development Outcome

The integrated application was tested using successful requests:

OPTIONS /api/interview 200 OK
POST /api/interview 200 OK

Multiple POST requests confirmed that the React frontend was communicating with the FastAPI backend.

16. Final Interview Flow

The final tested flow is:

Synthetic Candidate Profile
          |
          v
Candidate Profiler
          |
          v
Interview Plan
          |
          v
Question Generation
          |
          v
Candidate Answer
          |
          v
Answer Evaluation
          |
          +---- Follow-up Required ----+
          |                            |
          |                            v
          |                     Follow-up Question
          |                            |
          +-------------+--------------+
                        |
                        v
                  Next Question
                        |
                        v
                Interview Completion
                        |
                        v
               Structured Feedback
                        |
                        v
                  Results Screen
17. Final Development State

The implemented system provides:

Conversational technical interviewing
Minimum 8 questions
Coverage across multiple curriculum days
Adaptive follow-up questions
Session-based interview context
Candidate answer evaluation
Structured final feedback
Overall score
Strengths
Areas for improvement
Recommended next steps
React frontend
FastAPI backend
HTTP API integration

The project was developed iteratively with AI assistance for architecture, implementation, debugging, integration, and testing.