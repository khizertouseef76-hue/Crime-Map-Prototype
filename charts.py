import pandas as pd
import streamlit as st
import plotly.express as px
from utils.grading import grade_for_rate, grade_emoji

def render_charts(df: pd.DataFrame, selected_metric: str):
    """
    df: columns [crime_type, incidents, population, rate]
    """
    st.subheader("Crime breakdown", anchor=False)

    # Make grades
    df = df.copy()
    df["grade"], df["grade_color"] = zip(*df["rate"].map(grade_for_rate))
    df["grade_mark"] = df["grade"].map(grade_emoji)

    # Bar chart
    fig = px.bar(
        df,
        x="crime_type",
        y="rate",
        hover_data=["incidents", "population", "grade"],
        title="Rates per 100k by crime type",
        labels={"crime_type": "Crime Type", "rate": "Rate per 100k"},
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    # Grades table with export
    st.markdown("### Grades table")
    show_cols = ["crime_type", "incidents", "population", "rate", "grade_mark", "grade"]
    st.dataframe(df[show_cols], use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv,
        file_name="crime_metrics.csv",
        mime="text/csv",
    ) 