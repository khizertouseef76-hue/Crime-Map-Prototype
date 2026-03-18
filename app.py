import streamlit as st
import pandas as pd

from config import CRIME_API_KEY, CRIME_API_BASE, CRIME_METRICS, DEFAULT_ADDRESS, DEFAULT_ZIP, RADIUS_MILES
from services.geocode import geocode_address
from services.crime_api import fetch_crime_by_type, fetch_tracts_geojson, available_metrics
from components.map_view import render_map
from components.charts import render_charts

st.set_page_config(
    page_title="Crime Map — Local MVP",
    page_icon="🗺️",
    layout="wide",
)

# --- Header
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:12px;margin: 0 0 10px 0;">
      <div style="font-size:28px;font-weight:700;letter-spacing:.2px;">Crime Mapping (Local MVP)</div>
      <div style="background:#E0F2FE;color:#0369A1; padding:4px 10px;border-radius:999px;font-size:12px;">
        Streamlit
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar controls
with st.sidebar:
    st.header("Search", anchor=False)
    address_or_zip = st.text_input(
        "Address or ZIP code",
        value=DEFAULT_ADDRESS,
        help="Enter a US address or ZIP (e.g., '34689' or '123 Main St, City, ST')",
    )
    st.caption(f"API base: {CRIME_API_BASE} | Key loaded: {'✅' if CRIME_API_KEY else '❌'}")

    st.divider()

    st.header("Metric", anchor=False)
    metric_hint = st.caption("Pick a crime metric to color the map.")
    search_btn = st.button("Search", type="primary", use_container_width=True)

st.info(
    "Purpose: Localhost MVP that geocodes an address/ZIP, fetches crime data, "
    "renders tract polygons as a choropleth, and shows charts + grades.",
    icon="🎯",
)

# --- Perform search
if search_btn or "last_query" not in st.session_state:
    st.session_state["last_query"] = address_or_zip

query = st.session_state["last_query"]
col1, col2 = st.columns([1, 1])

with st.spinner("Geocoding location..."):
    geocoded = geocode_address(query)

if not geocoded:
    st.error("Could not geocode that location. Try a different address/ZIP.")
    st.stop()

lat, lon = geocoded

# Fetch data
with st.spinner("Fetching crime metrics..."):
    df = fetch_crime_by_type(query if query.strip().isdigit() else DEFAULT_ZIP)
    metrics = available_metrics(df)

with st.sidebar:
    selected_metric = st.selectbox("Crime metric (for map coloring)", options=metrics, index=0)

with st.spinner("Loading tract polygons..."):
    # Note: tract service is keyed by ZIP; if user typed full address we use default ZIP as a demo
    zip_for_map = query if query.strip().isdigit() else DEFAULT_ZIP
    gj = fetch_tracts_geojson(zip_for_map)

# --- Main map
st.subheader("Map", anchor=False)
render_map(
    geojson=gj,
    center=(lat, lon),
    selected_metric=selected_metric,
    radius_miles=RADIUS_MILES,
)

# --- Charts & Table
render_charts(df, selected_metric)

st.caption(
    "Data sources: FBI UCR / Local PD (via provided API). Rates normalized per 100k residents. "
    "This MVP includes a local fallback dataset for demonstration."
)
