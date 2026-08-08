def generate_question(day_data, question_number=1):
    """
    Generate a technical interview question from one curriculum day.
    """

    title = day_data.get("title", "")
    objectives = day_data.get("objectives", [])
    day = day_data.get("day")

    if not objectives:
        return {
            "day": day,
            "title": title,
            "question": f"Can you explain what you learned about {title}?",
            "difficulty": "intermediate"
        }

    # Use the first curriculum objective as the foundation.
    primary_objective = objectives[0]

    question = (
        f"Let's discuss {title}. "
        f"Can you explain how you would approach this in a real "
        f"AI engineering project, specifically considering that "
        f"you should {primary_objective.lower()}?"
    )

    return {
        "day": day,
        "title": title,
        "question": question,
        "difficulty": "intermediate",
        "objective": primary_objective
    }