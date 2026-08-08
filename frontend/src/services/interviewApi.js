const API_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function startInterview(sessionId, candidate) {
  const response = await fetch(`${API_URL}/api/interview`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      sessionId,
      candidate,
    }),
  });

  if (!response.ok) {
    throw new Error("Unable to start interview");
  }

  return response.json();
}

export async function sendAnswer(sessionId, message) {
  const response = await fetch(`${API_URL}/api/interview`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      sessionId,
      message,
    }),
  });

  if (!response.ok) {
    throw new Error("Unable to submit answer");
  }

  return response.json();
}