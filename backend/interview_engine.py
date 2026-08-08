def create_interview_plan(profile, minimum_questions=8):
    completed = profile.get("completed", [])

    if not completed:
        return []

    # Sort completed missions by day
    completed = sorted(
        completed,
        key=lambda mission: mission.get("day", 0)
    )

    plan = []

    # Prefer missions that the candidate completed confidently.
    # Lower attempts indicate stronger first-pass performance.
    prioritized = sorted(
        completed,
        key=lambda mission: (
            mission.get("attempts", 1),
            mission.get("day", 0)
        )
    )

    # Select different curriculum days first.
    selected_days = set()

    for mission in prioritized:
        day = mission.get("day")

        if day not in selected_days:
            plan.append({
                "day": day,
                "title": mission.get("title"),
                "attempts": mission.get("attempts", 1),
                "type": "primary"
            })

            selected_days.add(day)

        if len(plan) >= minimum_questions:
            break

    # If fewer than 8 unique completed missions exist,
    # reuse remaining completed missions as additional questions.
    if len(plan) < minimum_questions:

        for mission in completed:
            if len(plan) >= minimum_questions:
                break

            already_selected = any(
                item["day"] == mission.get("day")
                and item["title"] == mission.get("title")
                for item in plan
            )

            if not already_selected:
                plan.append({
                    "day": mission.get("day"),
                    "title": mission.get("title"),
                    "attempts": mission.get("attempts", 1),
                    "type": "secondary"
                })

    return plan