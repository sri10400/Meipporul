import { useState } from "react";
import "./App.css";

const candidate = {
  name: "Emily Chen",
  role: "AI Engineer",
  experience: "6 years experience",
};

const topics = [
  "RAG",
  "Vector Databases",
  "Agentic AI",
  "MCP",
  "Production AI",
];

const questions = [
  {
    topic: "RAG · Retrieval",
    text: "Your healthcare chatbot needs to choose between SQL, vector search, and hybrid retrieval. How would you design this?",
  },
  {
    topic: "Vector Databases",
    text: "How would you improve the quality of results returned by a vector database when the relevant document exists but is not being retrieved?",
  },
  {
    topic: "Agentic AI",
    text: "How would you design an AI agent that can decide when to use a tool and when to answer directly?",
  },
];

function App() {
  const [screen, setScreen] = useState("start");
  const [questionIndex, setQuestionIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [isEvaluating, setIsEvaluating] = useState(false);

  const currentQuestion = questions[questionIndex];

  const startInterview = () => {
    setScreen("interview");
  };

  const submitAnswer = () => {
    if (!answer.trim()) return;

    setIsEvaluating(true);

    setTimeout(() => {
      setIsEvaluating(false);
      setAnswer("");

      if (questionIndex < questions.length - 1) {
        setQuestionIndex((previous) => previous + 1);
      } else {
        setScreen("results");
      }
    }, 900);
  };

  const restartInterview = () => {
    setQuestionIndex(0);
    setAnswer("");
    setScreen("start");
  };

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

      {screen === "start" && (
        <main className="page start-page">
          <section className="hero-section">
            <div className="eyebrow">AI ENGINEERING INTERVIEW</div>

            <h1>
              Show what you
              <span> actually know.</span>
            </h1>

            <p className="hero-description">
              A personalized technical interview that adapts to your learning
              journey, answers, and technical depth.
            </p>

            <div className="candidate-card">
              <div className="avatar">EC</div>

              <div>
                <h2>{candidate.name}</h2>
                <p>
                  {candidate.role} · {candidate.experience}
                </p>
              </div>

              <div className="candidate-badge">COHORT</div>
            </div>

            <div className="section-label">INTERVIEW COVERAGE</div>

            <div className="topic-grid">
              {topics.map((topic, index) => (
                <div className="topic-chip" key={topic}>
                  <span className="topic-number">0{index + 1}</span>
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

            <button className="primary-button" onClick={startInterview}>
              Start interview
              <span>→</span>
            </button>

            <p className="privacy-note">
              Your interview is personalized from your cohort learning
              journey.
            </p>
          </section>
        </main>
      )}

      {screen === "interview" && (
        <main className="page interview-page">
          <div className="interview-header">
            <div>
              <div className="eyebrow">TECHNICAL INTERVIEW</div>
              <h1>{candidate.name}</h1>
              <p>{candidate.role}</p>
            </div>

            <div className="question-count">
              <strong>{questionIndex + 1}</strong>
              <span>/ 8+</span>
            </div>
          </div>

          <section className="journey-card">
            <div className="section-label">YOUR INTERVIEW JOURNEY</div>

            <div className="journey">
              <div className="journey-item completed">
                <span>✓</span>
                RAG
              </div>

              <div className="journey-line completed-line"></div>

              <div className="journey-item active">
                <span>→</span>
                {currentQuestion.topic.split(" · ")[0]}
              </div>

              <div className="journey-line"></div>

              <div className="journey-item">
                <span>○</span>
                MCP
              </div>

              <div className="journey-line"></div>

              <div className="journey-item">
                <span>○</span>
                Production
              </div>
            </div>
          </section>

          <section className="question-section">
            <div className="question-label">
              QUESTION {String(questionIndex + 1).padStart(2, "0")}
            </div>

            <div className="question-topic">{currentQuestion.topic}</div>

            <h2>{currentQuestion.text}</h2>

            <div className="answer-area">
              <div className="answer-label">YOUR RESPONSE</div>

              <textarea
                value={answer}
                onChange={(event) => setAnswer(event.target.value)}
                placeholder="Explain your approach, reasoning, and engineering decisions..."
                disabled={isEvaluating}
              />

              <div className="answer-footer">
                <span>{answer.trim().length} characters</span>

                <span>Be specific. Think like an engineer.</span>
              </div>
            </div>

            {isEvaluating ? (
              <div className="evaluating">
                <span className="loader"></span>
                Evaluating your response and preparing the next question...
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
              <span>Interview progress</span>
              <strong>{Math.round(((questionIndex + 1) / 8) * 100)}%</strong>
            </div>

            <div className="progress-track">
              <div
                className="progress-fill"
                style={{
                  width: `${Math.min(((questionIndex + 1) / 8) * 100, 100)}%`,
                }}
              ></div>
            </div>
          </div>
        </main>
      )}

      {screen === "results" && (
        <main className="page results-page">
          <section className="results-header">
            <div className="eyebrow">INTERVIEW COMPLETE</div>

            <div className="score-circle">
              <strong>82</strong>
              <span>/100</span>
            </div>

            <h1>Strong performance.</h1>

            <p>
              You demonstrated strong technical reasoning across modern AI
              engineering concepts.
            </p>
          </section>

          <section className="results-card">
            <div className="section-label">TECHNICAL AREAS</div>

            <ScoreRow name="RAG" score={91} />
            <ScoreRow name="Vector Search" score={78} />
            <ScoreRow name="Agentic AI" score={88} />
            <ScoreRow name="MCP" score={74} />
            <ScoreRow name="Production AI" score={69} />
          </section>

          <section className="feedback-grid">
            <div className="feedback-card">
              <div className="feedback-icon positive">+</div>
              <div>
                <div className="section-label">STRENGTHS</div>
                <ul>
                  <li>Strong RAG architecture understanding</li>
                  <li>Good reasoning around agent workflows</li>
                </ul>
              </div>
            </div>

            <div className="feedback-card">
              <div className="feedback-icon warning">!</div>
              <div>
                <div className="section-label">AREAS TO IMPROVE</div>
                <ul>
                  <li>MCP failure handling</li>
                  <li>Production deployment strategy</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="next-steps">
            <div className="section-label">RECOMMENDED NEXT STEPS</div>

            <div className="next-step">
              <span>01</span>
              <div>
                <strong>Review Day 24</strong>
                <p>MCP integration and failure handling</p>
              </div>
              <span>→</span>
            </div>

            <div className="next-step">
              <span>02</span>
              <div>
                <strong>Review Day 28</strong>
                <p>Deployment and production systems</p>
              </div>
              <span>→</span>
            </div>
          </section>

          <button className="secondary-button" onClick={restartInterview}>
            Take another interview
          </button>
        </main>
      )}

      <footer className="footer">
        <span>INTERVUEAI</span>
        <span>Adaptive technical interviews for AI engineers.</span>
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
        <div className="score-fill" style={{ width: `${score}%` }}></div>
      </div>
    </div>
  );
}

export default App;