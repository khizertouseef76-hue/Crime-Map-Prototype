from typing import Tuple

# Choropleth thresholds (per 100k residents)
# Based on your spec: Dark Red >1000, Red 500–999, Light Red 200–499, Pink <200, Grey no data
def rate_to_color(rate: float | None) -> Tuple[str, str]:
    """
    Returns (hex_color, label)
    """
    if rate is None:
        return ("#9CA3AF", "No data")   # Grey
    if rate > 1000:
        return ("#7F1D1D", "> 1000")    # Dark Red
    if rate >= 500:
        return ("#DC2626", "500 – 999") # Red
    if rate >= 200:
        return ("#F87171", "200 – 499") # Light Red
    if rate >= 0:
        return ("#FBCFE8", "< 200")     # Pink
    return ("#9CA3AF", "No data")

PALETTE = {
    "A": "#16A34A",
    "B": "#22C55E",
    "C": "#EAB308",
    "D": "#F59E0B",
    "F": "#DC2626",
}
