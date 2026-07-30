import streamlit as st
import pandas as pd

from src.database.connection import engine
from utils.ui import page_header, format_salary

st.title("Historical Trends")

page_header(
    "UK Labour Market Overview",
    "AI-powered analysis of UK job demand, skills and salary trends."
)

query = """
SELECT *
FROM vw_market_trends
"""


df = pd.read_sql(
    query,
    engine
)


# Date format

df["metric_date"] = pd.to_datetime(
    df["metric_date"]
)


# Metric selector

metrics = df["metric_type"].unique()


selected_metric = st.selectbox(
    "Metric",
    metrics
)


trend_df = df[
    df["metric_type"] == selected_metric
]


st.subheader(
    f"{selected_metric} Growth Over Time"
)


st.line_chart(
    trend_df.set_index(
        "metric_date"
    )["metric_value"]
)