import streamlit as st
import pandas as pd
import plotly.express as px

from connection import get_connection
from queries import COMPANY_SKILL_PROFILE_QUERY


st.set_page_config(
    page_title="Companies",
    page_icon="🏢",
    layout="wide"
)


# @st.cache_data
def load_data(query):

    engine = get_connection()

    return pd.read_sql(
        query,
        engine
    )


df = load_data(
    COMPANY_SKILL_PROFILE_QUERY
)


st.title(
    "🏢 Companies"
)


# -----------------------------
# Cleaning
# -----------------------------

df = df[
    df["company_name"].notna()
    & df["skill_name"].notna()
]


# -----------------------------
# Filters
# -----------------------------

col1, col2 = st.columns(2)


with col1:

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


with col2:

    companies = [
        "All"
    ] + sorted(
        df["company_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_company = st.selectbox(
        "Company",
        companies
    )


filtered = df.copy()


if selected_category != "All":

    filtered = filtered[
        filtered["skill_category"]
        == selected_category
    ]


if selected_company != "All":

    filtered = filtered[
        filtered["company_name"]
        == selected_company
    ]



# -----------------------------
# KPI Cards
# -----------------------------

company_summary = (
    filtered
    .groupby(
        "company_name",
        as_index=False
    )
    .agg(
        {
            "occurrences": "sum",
            "skill_name": "nunique",
            "median_salary": "median"
        }
    )
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Companies",
        f"{company_summary['company_name'].nunique():,}"
    )


with c2:

    st.metric(
        "Skills Covered",
        f"{filtered['skill_name'].nunique():,}"
    )


with c3:

    st.metric(
        "Total Demand",
        f"{filtered['occurrences'].sum():,}"
    )


with c4:

    st.metric(
        "Median Salary",
        f"£{filtered['median_salary'].median():,.0f}"
    )



st.divider()



# -----------------------------
# Hiring Demand
# -----------------------------

st.subheader(
    "📊 Hiring Demand by Company"
)


demand_df = (
    company_summary
    .sort_values(
        "occurrences",
        ascending=False
    )
    .head(20)
)


fig1 = px.bar(
    demand_df,
    x="occurrences",
    y="company_name",
    orientation="h",
    labels={
        "company_name": "Company",
        "occurrences": "Job Demand"
    },
    height=550
)


st.plotly_chart(
    fig1,
    use_container_width=True
)



# -----------------------------
# Skill Profile
# -----------------------------

st.divider()

st.subheader(
    "🧩 Company Skill Profile"
)


profile_df = (
    filtered
    .groupby(
        [
            "company_name",
            "skill_category"
        ],
        as_index=False
    )
    [
        "occurrences"
    ]
    .sum()
)


fig2 = px.bar(
    profile_df,
    x="company_name",
    y="occurrences",
    color="skill_category",
    labels={
        "company_name": "Company",
        "occurrences": "Skill Demand",
        "skill_category": "Skill Category"
    },
    height=500
)


st.plotly_chart(
    fig2,
    use_container_width=True
)



# -----------------------------
# Salary vs Demand Quadrant
# -----------------------------

st.divider()

st.subheader(
    "🎯 Company Market Position"
)


quadrant_df = (
    filtered
    .groupby(
        "company_name",
        as_index=False
    )
    .agg(
        {
            "occurrences": "sum",
            "median_salary": "median",
            "skill_name": "nunique"
        }
    )
)


fig3 = px.scatter(
    quadrant_df,
    x="occurrences",
    y="median_salary",
    size="skill_name",
    hover_name="company_name",
    labels={
        "occurrences": "Hiring Demand",
        "median_salary": "Median Salary",
        "skill_name": "Skill Diversity"
    },
    height=650
)


fig3.add_vline(
    x=quadrant_df["occurrences"].median(),
    line_dash="dash"
)


fig3.add_hline(
    y=quadrant_df["median_salary"].median(),
    line_dash="dash"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)



# -----------------------------
# Detail Table
# -----------------------------

st.divider()

st.subheader(
    "📋 Company Skill Details"
)


table = (
    filtered
    .sort_values(
        "occurrences",
        ascending=False
    )
    .head(100)
    .copy()
)


table.columns = [
    "Company",
    "Skill",
    "Skill Type",
    "Skill Category",
    "Demand",
    "Median Salary"
]


st.dataframe(
    table,
    hide_index=True,
    use_container_width=True
)