import streamlit as st
import pandas as pd
import plotly.express as px


from connection import get_connection
from queries import FORECASTING_MARKET_TREND_QUERY


st.set_page_config(
    page_title="Trends",
    page_icon="📈",
    layout="wide"
)


@st.cache_data
def load_data(query):

    engine = get_connection()

    return pd.read_sql(
        query,
        engine
    )


df = load_data(
    FORECASTING_MARKET_TREND_QUERY
)


# -----------------------------
# Data Cleaning
# -----------------------------

df["date"] = pd.to_datetime(
    df["date"]
)


# -----------------------------
# Title
# -----------------------------

st.title(
    "📈 Market Trends"
)


# -----------------------------
# Filters
# -----------------------------

col1, col2, col3 = st.columns(3)


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

    types = [
        "All"
    ] + sorted(
        df["skill_type"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_type = st.selectbox(
        "Skill Type",
        types
    )


with col3:

    skills = [
        "All"
    ] + sorted(
        df["skill_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_skill = st.selectbox(
        "Skill",
        skills
    )


filtered = df.copy()


if selected_category != "All":

    filtered = filtered[
        filtered["skill_category"]
        == selected_category
    ]


if selected_type != "All":

    filtered = filtered[
        filtered["skill_type"]
        == selected_type
    ]


if selected_skill != "All":

    filtered = filtered[
        filtered["skill_name"]
        == selected_skill
    ]



# -----------------------------
# KPI Cards
# -----------------------------

c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Skills Tracked",
        f"{filtered['skill_name'].nunique():,}"
    )


with c2:

    st.metric(
        "Total Job Demand",
        f"{filtered['job_count'].sum():,}"
    )


with c3:

    st.metric(
        "Median Salary",
        f"£{filtered['median_salary'].median():,.0f}"
    )



st.divider()



# -----------------------------
# Demand Trend
# -----------------------------

st.subheader(
    "📊 Skill Demand Over Time"
)


trend_df = (
    filtered
    .groupby(
        [
            "date",
            "skill_name"
        ],
        as_index=False
    )
    [
        "job_count"
    ]
    .sum()
)


fig1 = px.line(
    trend_df,
    x="date",
    y="job_count",
    color="skill_name",
    markers=True,
    labels={
        "date": "Date",
        "job_count": "Job Count",
        "skill_name": "Skill"
    }
)


st.plotly_chart(
    fig1,
    use_container_width=True
)



# -----------------------------
# Salary Trend
# -----------------------------

st.subheader(
    "💷 Salary Trend"
)


salary_df = (
    filtered
    .groupby(
        [
            "date",
            "skill_name"
        ],
        as_index=False
    )
    [
        "median_salary"
    ]
    .mean()
)


fig2 = px.line(
    salary_df,
    x="date",
    y="median_salary",
    color="skill_name",
    markers=True,
    labels={
        "date": "Date",
        "median_salary": "Median Salary",
        "skill_name": "Skill"
    }
)


fig2.update_yaxes(
    tickprefix="£"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)



# -----------------------------
# Quadrant Analysis
# -----------------------------

st.divider()


st.subheader(
    "🎯 Skill Market Position"
)


quadrant_df = (
    filtered
    .groupby(
        "skill_name",
        as_index=False
    )
    .agg(
        {
            "job_count": "sum",
            "median_salary": "median",
            "skill_category": "first"
        }
    )
)


fig3 = px.scatter(
    quadrant_df,
    x="job_count",
    y="median_salary",
    size="job_count",
    color="skill_category",
    hover_name="skill_name",
    labels={
        "job_count": "Demand (Job Count)",
        "median_salary": "Median Salary",
        "skill_category": "Category"
    },
    height=650
)


# Median lines

fig3.add_vline(
    x=quadrant_df["job_count"].median(),
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
# Top Skills Table
# -----------------------------

st.divider()


st.subheader(
    "🔥 Leading Skills"
)


table = (
    quadrant_df
    .sort_values(
        "job_count",
        ascending=False
    )
    .head(30)
)


table.columns = [
    "Skill",
    "Demand",
    "Median Salary",
    "Category"
]


st.dataframe(
    table,
    hide_index=True,
    use_container_width=True
)