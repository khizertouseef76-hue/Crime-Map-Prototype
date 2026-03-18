from utils.colors import PALETTE

def grade_for_rate(rate: float | None) -> tuple[str, str]:
    """
    Convert a rate per 100k into (grade, color_hex), A–F.
    Tune thresholds as needed.
    """
    if rate is None:
        return "N/A", "#9CA3AF"
    if rate < 100:
        return "A", PALETTE["A"]
    if rate < 200:
        return "B", PALETTE["B"]
    if rate < 400:
        return "C", PALETTE["C"]
    if rate < 700:
        return "D", PALETTE["D"]
    return "F", PALETTE["F"]

def grade_emoji(grade: str) -> str:
    return {
        "A": "🟩",
        "B": "🟩",
        "C": "🟨",
        "D": "🟧",
        "F": "🟥",
    }.get(grade, "⬜")
