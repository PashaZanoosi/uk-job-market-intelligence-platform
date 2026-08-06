import streamlit as st
import pandas as pd
import plotly.express as px

from connection import get_connection
from queries import SKILL_SALARY_RANGE_QUERY


st.set_page_config(
    page_title="Skills",
    page_icon="🎯",
    layout="wide"
)


@st.cache_data
def load_data(query):
    engine = get_connection()
    return pd.read_sql(query, engine)


df = load_data(SKILL_SALARY_RANGE_QUERY)


st.title("🎯 Skills Market Value")


# -----------------------------
# Clean data
# -----------------------------

df = df[
    df["skill_name"].notna()
    & (df["skill_name"].str.strip() != "")
]


# -----------------------------
# KPI Cards
# -----------------------------

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Total Skills",
        f"{df['skill_name'].nunique():,}"
    )


with col2:
    top_skill = (
        df.sort_values(
            "demand",
            ascending=False
        )
        .iloc[0]
    )

    st.metric(
        "Most Demanded",
        top_skill["skill_name"]
    )


with col3:
    salary_skill = (
        df.sort_values(
            "salary_median",
            ascending=False
        )
        .iloc[0]
    )

    st.metric(
        "Highest Median Salary",
        f"£{salary_skill['salary_median']:,.0f}"
    )



st.divider()


# -----------------------------
# Filters
# -----------------------------

col1, col2 = st.columns(2)


with col1:
    skill_types = [
        "All"
    ] + sorted(
        df["skill_type"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_type = st.selectbox(
        "Skill Type",
        skill_types
    )


with col2:
    categories = [
        "All"
    ] + sorted(
        df["skill_category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.selectbox(
        "Skill Category",
        categories
    )


filtered = df.copy()


if selected_type != "All":
    filtered = filtered[
        filtered["skill_type"] == selected_type
    ]


if selected_category != "All":
    filtered = filtered[
        filtered["skill_category"] == selected_category
    ]


# -----------------------------
# Scatter Quadrant
# -----------------------------

st.subheader("Skill Demand vs Salary Opportunity")


fig = px.scatter(
    filtered,
    x="demand",
    y="salary_median",
    size="demand",
    color="skill_category",
    hover_name="skill_name",
    hover_data=[
        "skill_type",
        "salary_min",
        "salary_max",
        "salary_average"
    ],
    labels={
        "demand": "Job Demand",
        "salary_median": "Median Salary (£)",
        "skill_category": "Category"
    },
    height=600
)


# Add median lines for quadrant

fig.add_vline(
    x=filtered["demand"].median(),
    line_dash="dash"
)

fig.add_hline(
    y=filtered["salary_median"].median(),
    line_dash="dash"
)


fig.update_layout(
    legend_title_text="Skill Category"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


st.divider()


# -----------------------------
# Skill Table
# -----------------------------

st.subheader("Skill Salary Profile")


table = filtered[
    [
        "skill_name",
        "skill_type",
        "skill_category",
        "demand",
        "salary_min",
        "salary_max",
        "salary_average"
    ]
].copy()


table.columns = [
    "Skill",
    "Type",
    "Category",
    "Demand",
    "Min Salary",
    "Max Salary",
    "Average Salary"
]


st.dataframe(
    table,
    use_container_width=True,
    hide_index=True
)