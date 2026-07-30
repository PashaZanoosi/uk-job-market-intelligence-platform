import streamlit as st
import pandas as pd

from src.database.connection import engine
from utils.ui import page_header, format_salary

st.title("Market Analysis")


page_header(
    "UK Labour Market Overview",
    "AI-powered analysis of UK job demand, skills and salary trends."
)

query = """
SELECT *
FROM vw_market_breakdown
"""


df = pd.read_sql(
    query,
    engine
)

df = df[
    df["entity"] != "UK"
]

st.sidebar.header("Filters")


breakdowns = sorted(
    df["breakdown_type"]
    .dropna()
    .unique()
    .tolist()
)


selected_breakdown = st.sidebar.selectbox(
    "View By",
    breakdowns
)


filtered_df = df[
    df["breakdown_type"] == selected_breakdown
]


# KPI

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Entities",
    f"{filtered_df['entity'].nunique():,}"
)


col2.metric(
    "Jobs",
    f"{filtered_df['job_count'].sum():,}"
)


col3.metric(
    "Companies",
    f"{filtered_df['company_count'].sum():,}"
)


col4.metric(
    "Average Salary",
    f"£{filtered_df['average_salary'].mean():,.0f}"
)



# Top entities by demand

st.subheader(
    f"Top {selected_breakdown} by Job Demand"
)


top_demand = (
    filtered_df
    .sort_values(
        "job_count",
        ascending=False
    )
    .head(20)
)


st.bar_chart(
    top_demand.set_index(
        "entity"
    )["job_count"]
)



# Highest salary

st.subheader(
    f"Highest Paying {selected_breakdown}"
)


top_salary = (
    filtered_df
    .sort_values(
        "average_salary",
        ascending=False
    )
    .head(20)
)


st.bar_chart(
    top_salary.set_index(
        "entity"
    )["average_salary"]
)