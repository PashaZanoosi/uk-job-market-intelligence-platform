import streamlit as st
import pandas as pd

from src.database.connection import engine
from utils.ui import page_header, format_salary

st.title("Skills Intelligence")


page_header(
    "UK Labour Market Overview",
    "AI-powered analysis of UK job demand, skills and salary trends."
)

query = """
SELECT *
FROM vw_skill_market_summary
"""


df = pd.read_sql(
    query,
    engine
)


st.sidebar.header("Filters")


# Category Filter

categories = [
    "All"
] + sorted(
    df["category"]
    .dropna()
    .unique()
    .tolist()
)


selected_category = st.sidebar.selectbox(
    "Skill Category",
    categories
)


filtered_df = df.copy()


if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]


# Skill Filter

skills = [
    "All"
] + sorted(
    filtered_df["skill_name"]
    .dropna()
    .unique()
    .tolist()
)


selected_skill = st.sidebar.selectbox(
    "Skill",
    skills
)



# -------------------------
# Skill Detail Mode
# -------------------------

if selected_skill != "All":

    skill_df = filtered_df[
        filtered_df["skill_name"] == selected_skill
    ]


    st.subheader(
        f"{selected_skill} Analysis"
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Jobs",
        f"{skill_df['job_count'].sum():,}"
    )


    col2.metric(
        "Companies",
        f"{skill_df['company_count'].sum():,}"
    )


    col3.metric(
        "Locations",
        f"{skill_df['location_count'].sum():,}"
    )


    col4.metric(
        "Average Salary",
        f"£{skill_df['average_salary'].mean():,.0f}"
    )


    col5, col6, col7 = st.columns(3)


    col5.metric(
        "Minimum Salary",
        f"£{skill_df['min_salary'].min():,.0f}"
    )


    col6.metric(
        "Average Salary",
        f"£{skill_df['average_salary'].mean():,.0f}"
    )


    col7.metric(
        "Maximum Salary",
        f"£{skill_df['max_salary'].max():,.0f}"
    )



# -------------------------
# Ranking Mode
# -------------------------

else:


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Skills",
        f"{filtered_df['skill_name'].nunique():,}"
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



    st.subheader(
        "Top Skills by Demand"
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
            "skill_name"
        )["job_count"]
    )



    st.subheader(
        "Highest Paying Skills"
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
            "skill_name"
        )["average_salary"]
    )