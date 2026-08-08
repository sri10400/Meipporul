def build_candidate_profile(candidate):
    member = candidate.get("member", {})
    missions = candidate.get("missions", [])
    signals = candidate.get("signals", {})

    completed = []
    failed = []
    skipped = []

    for mission in missions:
        day = mission.get("day")
        title = mission.get("title", "")
        
        if mission.get("skipped") is True:
            skipped.append({
                "day": day,
                "title": title
            })

        elif mission.get("passed") is True:
            completed.append({
                "day": day,
                "title": title,
                "attempts": mission.get("attempts", 1)
            })

        else:
            failed.append({
                "day": day,
                "title": title,
                "attempts": mission.get("attempts", 1)
            })

    strengths = [
        mission["title"]
        for mission in completed
        if mission["attempts"] <= 2
    ]

    weak_areas = [
        mission["title"]
        for mission in failed
    ]

    weak_areas.extend(
        mission["title"]
        for mission in skipped
    )

    missions_completed = signals.get(
        "missionsCompleted",
        len(completed)
    )

    missions_first_try = signals.get(
        "missionsFirstTry",
        0
    )

    if missions_first_try >= 20:
        difficulty = "advanced"
    elif missions_first_try >= 10:
        difficulty = "intermediate"
    else:
        difficulty = "foundational"

    return {
        "candidate_id": member.get("id"),
        "name": member.get("name"),
        "role": member.get("jobRole"),
        "experience": member.get("yearsExperience"),
        "education": member.get("education"),
        "status": member.get("status"),

        "completed": completed,
        "failed": failed,
        "skipped": skipped,

        "strengths": strengths,
        "weak_areas": weak_areas,

        "signals": {
            "commit_days": signals.get("commitDays", 0),
            "missions_completed": missions_completed,
            "missions_first_try": missions_first_try
        },

        "recommended_difficulty": difficulty
    }