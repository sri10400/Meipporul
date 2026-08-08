import json
from pathlib import Path


CURRICULUM_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "curriculum.json"
)


def load_curriculum():
    with open(CURRICULUM_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def get_day(day_number):
    curriculum = load_curriculum()

    for day in curriculum.get("days", []):
        if day.get("day") == day_number:
            return day

    return None