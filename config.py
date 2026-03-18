import streamlit as st
import os

def _safe_secret(key: str, default: str = ""):
    try:
        return st.secrets[key] if key in st.secrets else default
    except FileNotFoundError:
        return default

CRIME_API_BASE = (
    os.getenv("CRIME_API_BASE")
    or _safe_secret("CRIME_API_BASE", "https://api.example.com")
)

CRIME_API_KEY = (
    os.getenv("CRIME_API_KEY")
    or _safe_secret("CRIME_API_KEY", "KMH73mYD0YUpCjydWBXzfFfBRMaId6VU6Wezs9Xr")
)

REQUEST_TIMEOUT = 12

CRIME_METRICS = [
    "violent_crime",
    "property_crime",
    "burglary",
    "larceny_theft",
    "motor_vehicle_theft",
    "aggravated_assault",
    "robbery",
    "rape",
    "homicide",
]

DEFAULT_ZIP = "34689"
DEFAULT_ADDRESS = "Tarpon Springs, FL"
DEFAULT_ZOOM = 12
RADIUS_MILES = 1.0      