def evaluate_answer(answer, question, objective):
    """
    Evaluate a candidate answer using simple heuristic signals.

    This is the baseline evaluator.
    Later, an LLM can provide deeper semantic evaluation.
    """

    if not answer or not answer.strip():
        return {
            "score": 0,
            "level": "weak",
            "reason": "No meaningful answer was provided.",
            "follow_up_needed": True
        }

    text = answer.strip()
    words = text.split()
    word_count = len(words)

    # Very short answers
    if word_count < 10:
        return {
            "score": 1,
            "level": "weak",
            "reason": "The answer is too brief to demonstrate sufficient technical understanding.",
            "follow_up_needed": True
        }

    # Basic technical signal detection
    technical_terms = [
        "because",
        "architecture",
        "system",
        "model",
        "data",
        "retrieval",
        "embedding",
        "vector",
        "api",
        "agent",
        "mcp",
        "docker",
        "kubernetes",
        "prompt",
        "database",
        "llm"
    ]

    lower_answer = text.lower()

    matched_terms = [
        term
        for term in technical_terms
        if term in lower_answer
    ]

    # Stronger answers contain enough detail and technical vocabulary
    if word_count >= 40 and len(matched_terms) >= 3:
        return {
            "score": 4,
            "level": "strong",
            "reason": "The answer provides sufficient detail and contains relevant technical concepts.",
            "follow_up_needed": True
        }

    # Moderate answer
    if word_count >= 20 and len(matched_terms) >= 1:
        return {
            "score": 3,
            "level": "partial",
            "reason": "The answer demonstrates some understanding but could use more technical depth.",
            "follow_up_needed": True
        }

    return {
        "score": 2,
        "level": "partial",
        "reason": "The answer shows limited understanding and needs clarification.",
        "follow_up_needed": True
    }
def generate_final_feedback(session):
    evaluations = list(session.scores.values())

    if not evaluations:
        return {
            "overall_score": 0,
            "performance": "No evaluation data available.",
            "strengths": [],
            "areas_to_improve": [],
            "recommendation": "Complete the interview to receive detailed feedback."
        }

    total_score = sum(
        evaluation.get("score", 0)
        for evaluation in evaluations
    )

    max_score = len(evaluations) * 4

    overall_score = round(
        (total_score / max_score) * 100
    )

    strengths = []
    improvements = []

    for evaluation in evaluations:
        level = evaluation.get("level")
        reason = evaluation.get("reason")

        if level == "strong":
            if reason and reason not in strengths:
                strengths.append(reason)

        elif level in ["partial", "weak"]:
            if reason and reason not in improvements:
                improvements.append(reason)

    if overall_score >= 80:
        performance = "Strong technical performance."
        recommendation = (
            "Continue practicing system design and "
            "advanced production-level scenarios."
        )

    elif overall_score >= 60:
        performance = "Good foundation with some areas to strengthen."
        recommendation = (
            "Review weaker concepts and practice explaining "
            "technical decisions in greater depth."
        )

    else:
        performance = "Foundational understanding needs improvement."
        recommendation = (
            "Revisit the core curriculum topics and practice "
            "explaining concepts with concrete examples."
        )

    return {
        "overall_score": overall_score,
        "performance": performance,
        "strengths": strengths,
        "areas_to_improve": improvements,
        "recommendation": recommendation
    }