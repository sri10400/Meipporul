import { useState } from "react";
import {
  startInterview as startInterviewApi,
  sendAnswer,
} from "./services/interviewApi";
import "./App.css";

const candidate = {
  name: "Emily Chen",
  role: "AI Engineer",
  experience: "6 years experience",

  // Candidate data expected by the FastAPI backend
  member: {
    id: "candidate-emily-001",
    name: "Emily Chen",
    jobRole: "AI Engineer",
    yearsExperience: 6,
    education: "Computer Science",
    status: "active",
  },

  missions: [
    {
      day: 1,
      title: "Embeddings Explained",
      passed: true,
      attempts: 1,
    },
    {
      day: 2,
      title: "Vector Databases Overview",
      passed: true,
      attempts: 1,
    },
    {
      day: 3,
      title: "The Retrieval & Matching Engine",
      passed: true,
      attempts: 2,
    },
    {
      day: 4,
      title: "RAG End-to-End & LLM API Basics",
      passed: true,
      attempts: 2,
    },
    {
      day: 5,
      title: "Prompt Engineering Fundamentals",
      passed: true,
      attempts: 1,
    },
    {
      day: 6,
      title: "Advanced Prompting: Function Calling",
      passed: true,
      attempts: 2,
    },
    {
      day: 7,
      title: "Agentic Frameworks: LangChain Agents",
      passed: true,
      attempts: 2,
    },
    {
      day: 8,
      title: "Multi-Agent Orchestration",
      passed: true,
      attempts: 2,
    },
  ],

  signals: {
    commitDays: 31,
    missionsCompleted: 8,
    missionsFirstTry: 4,
  },
};

const topics = [
  "RAG",
  "Vector Databases",
  "Agentic AI",
  "MCP",
  "Production AI",
];

function App() {
  const [screen, setScreen] = useState("start");
  const [questionIndex, setQuestionIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [error, setError] = useState("");

  const [sessionId, setSessionId] = useState("");
  const [currentQuestion, setCurrentQuestion] = useState("");
  const [feedback, setFeedback] = useState(null);

  const handleStartInterview = async () => {
    try {
      setError("");
      setFeedback(null);
      setAnswer("");
      setQuestionIndex(0);
      setIsEvaluating(true);

      const newSessionId = `session-${Date.now()}`;

      console.log("STARTING BACKEND INTERVIEW...");

      const response = await startInterviewApi(
        newSessionId,
        candidate
      );

      console.log("BACKEND START RESPONSE:", response);

      if (!response || !response.reply) {
        throw new Error(
          "Backend did not return the first interview question."
        );
      }

      setSessionId(newSessionId);
      setCurrentQuestion(response.reply);
      setScreen("interview");
    } catch (error) {
      console.error("START INTERVIEW ERROR:", error);

      setError(
        error.message || "Unable to start interview."
      );
    } finally {
      setIsEvaluating(false);
    }
  };

  const submitAnswer = async () => {
    if (!answer.trim()) {
      setError(
        "Please provide an answer before continuing."
      );
      return;
    }

    if (!sessionId) {
      setError(
        "Interview session is not available. Please restart the interview."
      );
      return;
    }

    try {
      setError("");
      setIsEvaluating(true);

      console.log("SENDING ANSWER TO BACKEND...");

      const response = await sendAnswer(
        sessionId,
        answer
      );

      console.log(
        "BACKEND ANSWER RESPONSE:",
        response
      );

      setAnswer("");

      if (response.done) {
        setFeedback(response.feedback || null);
        setScreen("results");
        return;
      }

      if (!response.reply) {
        throw new Error(
          "Backend did not return the next question."
        );
      }

      setCurrentQuestion(response.reply);

      setQuestionIndex(
        (previous) => previous + 1
      );
    } catch (error) {
      console.error(
        "SUBMIT ANSWER ERROR:",
        error
      );

      setError(
        error.message ||
          "Unable to submit your answer."
      );
    } finally {
      setIsEvaluating(false);
    }
  };

  const restartInterview = () => {
    setQuestionIndex(0);
    setAnswer("");
    setSessionId("");
    setCurrentQuestion("");
    setFeedback(null);
    setError("");
    setIsEvaluating(false);
    setScreen("start");
  };

  const overallScore =
    feedback?.overall_score ?? 0;

  const strengths =
    feedback?.strengths || [];

  const areasToImprove =
    feedback?.areas_to_improve || [];

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">I</span>
          <span>IntervueAI</span>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          AI Interviewer
        </div>
      </header>

      {/* =========================
          START SCREEN
      ========================= */}

      {screen === "start" && (
        <main className="page start-page">
          <section className="hero-section">
            <div className="eyebrow">
              AI ENGINEERING INTERVIEW
            </div>

            <h1>
              Show what you
              <span> actually know.</span>
            </h1>

            <p className="hero-description">
              A personalized technical interview
              that adapts to your learning journey,
              answers, and technical depth.
            </p>

            <div className="candidate-card">
              <div className="avatar">EC</div>

              <div>
                <h2>{candidate.name}</h2>

                <p>
                  {candidate.role} ·{" "}
                  {candidate.experience}
                </p>
              </div>

              <div className="candidate-badge">
                COHORT
              </div>
            </div>

            <div className="section-label">
              INTERVIEW COVERAGE
            </div>

            <div className="topic-grid">
              {topics.map((topic, index) => (
                <div
                  className="topic-chip"
                  key={topic}
                >
                  <span className="topic-number">
                    0{index + 1}
                  </span>

                  {topic}
                </div>
              ))}
            </div>

            <div className="interview-meta">
              <div>
                <strong>8+</strong>
                <span>Questions</span>
              </div>

              <div>
                <strong>Adaptive</strong>
                <span>Difficulty</span>
              </div>

              <div>
                <strong>31 days</strong>
                <span>Learning context</span>
              </div>
            </div>

            {error && (
              <div className="error-message">
                <span>!</span>
                {error}
              </div>
            )}

            <button
              className="primary-button"
              onClick={handleStartInterview}
              disabled={isEvaluating}
            >
              {isEvaluating
                ? "Starting interview..."
                : "Start interview"}

              <span>→</span>
            </button>

            <p className="privacy-note">
              Your interview is personalized from
              your cohort learning journey.
            </p>
          </section>
        </main>
      )}

      {/* =========================
          INTERVIEW SCREEN
      ========================= */}

      {screen === "interview" && (
        <main className="page interview-page">
          <div className="interview-header">
            <div>
              <div className="eyebrow">
                TECHNICAL INTERVIEW
              </div>

              <h1>{candidate.name}</h1>

              <p>{candidate.role}</p>
            </div>

            <div className="question-count">
              <strong>
                {questionIndex + 1}
              </strong>

              <span>/ 8+</span>
            </div>
          </div>

          <section className="journey-card">
            <div className="section-label">
              YOUR INTERVIEW JOURNEY
            </div>

            <div className="journey">
              {topics.map((topic, index) => {
                const isCompleted =
                  index < questionIndex;

                const isActive =
                  index === questionIndex;

                return (
                  <div
                    key={topic}
                    className="journey-wrapper"
                  >
                    <div
                      className={`journey-item ${
                        isCompleted
                          ? "completed"
                          : ""
                      } ${
                        isActive
                          ? "active"
                          : ""
                      }`}
                    >
                      <span>
                        {isCompleted
                          ? "✓"
                          : isActive
                          ? "→"
                          : "○"}
                      </span>

                      {topic}
                    </div>

                    {index <
                      topics.length - 1 && (
                      <div
                        className={`journey-line ${
                          isCompleted
                            ? "completed-line"
                            : ""
                        }`}
                      ></div>
                    )}
                  </div>
                );
              })}
            </div>
          </section>

          <section className="question-section">
            <div className="question-label">
              QUESTION{" "}
              {String(
                questionIndex + 1
              ).padStart(2, "0")}
            </div>

            <div className="question-topic">
              ADAPTIVE TECHNICAL QUESTION
            </div>

            <h2>
              {currentQuestion ||
                "Preparing your question..."}
            </h2>

            <div className="answer-area">
              <div className="answer-label">
                YOUR RESPONSE
              </div>

              <textarea
                value={answer}
                onChange={(event) => {
                  setAnswer(
                    event.target.value
                  );
                  setError("");
                }}
                placeholder="Explain your approach, reasoning, trade-offs, and engineering decisions..."
                disabled={isEvaluating}
              />

              <div className="answer-footer">
                <span>
                  {answer.trim().length} characters
                </span>

                <span>
                  Be specific. Think like an engineer.
                </span>
              </div>
            </div>

            {error && (
              <div className="error-message">
                <span>!</span>
                {error}
              </div>
            )}

            {isEvaluating ? (
              <div className="evaluating">
                <span className="loader"></span>

                <div>
                  <strong>
                    Analyzing your response
                  </strong>

                  <p>
                    Evaluating technical depth
                    and preparing your next
                    question.
                  </p>
                </div>
              </div>
            ) : (
              <button
                className="primary-button submit-button"
                onClick={submitAnswer}
                disabled={!answer.trim()}
              >
                Submit answer
                <span>→</span>
              </button>
            )}
          </section>

          <div className="progress-section">
            <div className="progress-info">
              <span>
                Interview progress
              </span>

              <strong>
                {Math.min(
                  questionIndex + 1,
                  8
                )}
                /8+
              </strong>
            </div>

            <div className="progress-track">
              <div
                className="progress-fill"
                style={{
                  width: `${Math.min(
                    ((questionIndex + 1) /
                      8) *
                      100,
                    100
                  )}%`,
                }}
              ></div>
            </div>
          </div>
        </main>
      )}

      {/* =========================
          RESULTS SCREEN
      ========================= */}

      {screen === "results" && (
        <main className="page results-page">
          <section className="results-header">
            <div className="eyebrow">
              INTERVIEW COMPLETE
            </div>

            <div className="result-status">
              <span>✓</span>{" "}
              Technical interview completed
            </div>

            <div className="score-circle">
              <strong>
                {overallScore}
              </strong>

              <span>/100</span>
            </div>

            <h1>
              {feedback?.performance ||
                "Interview completed."}
            </h1>

            <p>
              {feedback?.recommendation ||
                "Your interview has been evaluated based on your technical explanations, reasoning, and understanding of the covered topics."}
            </p>
          </section>

          {/* TECHNICAL PERFORMANCE */}

          <section className="results-card">
            <div className="section-heading">
              <div>
                <div className="section-label">
                  TECHNICAL PERFORMANCE
                </div>

                <p>
                  How you performed across the
                  interview.
                </p>
              </div>

              <span className="overall-score">
                {overallScore}%
              </span>
            </div>

            <ScoreRow
              name="Overall Technical Performance"
              score={overallScore}
            />
          </section>

          {/* FEEDBACK */}

          <section className="feedback-grid">
            {/* STRENGTHS */}

            <div className="feedback-card">
              <div className="feedback-icon positive">
                +
              </div>

              <div>
                <div className="section-label">
                  STRENGTHS
                </div>

                {strengths.length > 0 ? (
                  <ul>
                    {strengths.map(
                      (strength, index) => (
                        <li key={index}>
                          {strength}
                        </li>
                      )
                    )}
                  </ul>
                ) : (
                  <p>
                    No specific strengths were
                    identified in this interview.
                  </p>
                )}
              </div>
            </div>

            {/* AREAS TO IMPROVE */}

            <div className="feedback-card">
              <div className="feedback-icon warning">
                !
              </div>

              <div>
                <div className="section-label">
                  AREAS TO IMPROVE
                </div>

                {areasToImprove.length >
                0 ? (
                  <ul>
                    {areasToImprove.map(
                      (area, index) => (
                        <li key={index}>
                          {area}
                        </li>
                      )
                    )}
                  </ul>
                ) : (
                  <p>
                    No major improvement areas
                    identified.
                  </p>
                )}
              </div>
            </div>
          </section>

          {/* RECOMMENDED NEXT STEPS */}

          <section className="next-steps">
            <div className="section-label">
              RECOMMENDED NEXT STEP
            </div>

            <div className="next-step">
              <span>01</span>

              <div>
                <strong>
                  Continue building your
                  technical depth
                </strong>

                <p>
                  {feedback?.recommendation ||
                    "Review the interview topics and continue practicing technical explanations."}
                </p>
              </div>

              <span>→</span>
            </div>
          </section>

          {/* ACTIONS */}

          <div className="results-actions">
            <button
              className="primary-button"
              onClick={restartInterview}
            >
              Take another interview
              <span>→</span>
            </button>

            <button className="secondary-button">
              View interview summary
            </button>
          </div>
        </main>
      )}

      <footer className="footer">
        <span>INTERVUEAI</span>

        <span>
          Adaptive technical interviews for AI
          engineers.
        </span>
      </footer>
    </div>
  );
}

function ScoreRow({ name, score }) {
  return (
    <div className="score-row">
      <div className="score-row-header">
        <span>{name}</span>

        <strong>{score}%</strong>
      </div>

      <div className="score-track">
        <div
          className="score-fill"
          style={{
            width: `${score}%`,
          }}
        ></div>
      </div>
    </div>
  );
}

export default App;