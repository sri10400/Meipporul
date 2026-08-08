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