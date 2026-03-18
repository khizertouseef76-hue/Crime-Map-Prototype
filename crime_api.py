import requests
import pandas as pd
import json
import pathlib
from config import CRIME_API_KEY, CRIME_API_BASE

DATA_DIR = pathlib.Path(__file__).resolve().parents[1] / "data"

def fetch_crime_by_type(zip_code: str) -> pd.DataFrame:
    url = f"{CRIME_API_BASE.rstrip('/')}/crime-data"
    headers = {"Authorization": f"Bearer {CRIME_API_KEY}"}
    try:
        r = requests.post(url, json={"zip_code": zip_code}, headers=headers, timeout=10)
        r.raise_for_status()
        return pd.DataFrame(r.json())
    except Exception as e:
        print("API error:", e)
        return pd.read_csv(DATA_DIR / "sample_crime_by_type.csv")

def fetch_tracts_geojson(zip_code: str) -> dict:
    url = f"{CRIME_API_BASE.rstrip('/')}/tracts/{zip_code}"
    headers = {"Authorization": f"Bearer {CRIME_API_KEY}"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("GeoJSON error:", e)
        with open(DATA_DIR / f"sample_tracts_{zip_code}.geojson", "r", encoding="utf-8") as f:
            return json.load(f)

def available_metrics(df: pd.DataFrame):
    """
    Return list of available crime metrics in the DataFrame.
    Used to populate the dropdown in Streamlit.
    """
    if "crime_type" not in df.columns:
        return []
    return df["crime_type"].dropna().unique().tolist() 