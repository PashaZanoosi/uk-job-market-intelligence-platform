import streamlit as st
import pandas as pd

from connection import get_connection
from queries import (
    TOP_SKILLS_QUERY,
    JOB_CATEGORY_QUERY
)


st.set_page_config(
    page_title="Overview",
    layout="wide"
)


# @st.cache_data
def load_data(query):
    engine = get_connection()
    return pd.read_sql(query, engine)


# -------------------------
# Load data
# -------------------------

top_skills_df = load_data(TOP_SKILLS_QUERY)
category_df = load_data(JOB_CATEGORY_QUERY)


# -------------------------
# Header
# -------------------------

st.title("🌍 Overview")
st.caption("UK Labour Market Intelligence Platform")


# -------------------------
# KPI Cards
# -------------------------

total_jobs = category_df["job_count"].sum()

top_skill = (
    top_skills_df.iloc[0]["skill_name"]
    if len(top_skills_df) > 0
    else "N/A"
)

median_salary = (
    int(top_skills_df.iloc[0]["median_salary"])
    if len(top_skills_df) > 0
    and pd.notna(top_skills_df.iloc[0]["median_salary"])
    else 0
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Jobs",
        f"{total_jobs:,}"
    )

with col2:
    st.metric(
        "Most Demanded Skill",
        top_skill
    )

with col3:
    st.metric(
        "Median Salary",
        f"£{median_salary:,.0f}"
    )


st.divider()


# -------------------------
# Top Skills Section
# -------------------------

st.subheader("🎯 Top Skills")


top_display = top_skills_df.head(10).copy()

top_display.insert(
    0,
    "No.",
    range(1, len(top_display) + 1)
)

top_display = top_display.drop(
    columns=[
        "min_salary",
    ],
    errors="ignore"
)

top_display = top_display.rename(
    columns={
        "skill_name": "Skill",
        "skill_type": "Skill Type",
        "skill_category": "Skill Category",
        "demand": "Number of Jobs",
        "median_salary": "Median Salary",
        "avg_salary": "Average Salary",
        "max_salary": "Maximum Salary",
    }
)


if "Median Salary" in top_display.columns:
    top_display["Median Salary"] = (
        top_display["Median Salary"]
        .apply(lambda x: f"£{x:,.0f}" if pd.notna(x) else "-")
    )


st.dataframe(
    top_display,
    use_container_width=True,
    hide_index=True
)


# -------------------------
# Job Categories Section
# -------------------------

st.subheader("📊 Job Categories")


category_display = category_df.copy()

category_display.insert(
    0,
    "No.",
    range(1, len(category_display) + 1)
)

category_display = category_display.drop(
    columns=[
        "min_salary",
    ],
    errors="ignore"
)

category_display = category_display.rename(
    columns={
        "category_label": "Job Category",
        "job_count": "Number of Jobs",
        "avg_salary": "Average Salary",
        "min_salary": "Minimum Salary",
        "max_salary": "Maximum Salary",
    }
)


columns_to_remove = [
    "min_salary",
    "salary_min"
]


for col in columns_to_remove:
    if col in category_display.columns:
        category_display = category_display.drop(columns=[col])


if "Average Salary" in category_display.columns:
    category_display["Average Salary"] = (
        category_display["Average Salary"]
        .apply(lambda x: f"£{x:,.0f}" if pd.notna(x) else "-")
    )


if "Maximum Salary" in category_display.columns:
    category_display["Maximum Salary"] = (
        category_display["Maximum Salary"]
        .apply(lambda x: f"£{x:,.0f}" if pd.notna(x) else "-")
    )


st.dataframe(
    category_display,
    use_container_width=True,
    hide_index=True
)