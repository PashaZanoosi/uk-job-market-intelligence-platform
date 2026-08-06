import streamlit as st
import pandas as pd
import plotly.express as px

from connection import get_connection
from queries import (
    SKILL_CATEGORY_QUERY,
    SKILL_SALARY_RANGE_QUERY,
    COMPANY_SKILL_PROFILE_QUERY,
    LOCATION_SKILL_SALARY_QUERY
)

from utils.geocoder import add_coordinates


st.set_page_config(
    page_title="Explorer",
    page_icon="🔍",
    layout="wide"
)


# @st.cache_data
def load_data(query):
    engine = get_connection()
    return pd.read_sql(query, engine)


# -----------------------------
# Load Data
# -----------------------------

skill_df = load_data(SKILL_CATEGORY_QUERY)

salary_df = load_data(SKILL_SALARY_RANGE_QUERY)

company_df = load_data(COMPANY_SKILL_PROFILE_QUERY)

location_df = load_data(LOCATION_SKILL_SALARY_QUERY)


# -----------------------------
# Clean Data
# -----------------------------

skill_df = skill_df[
    skill_df["skill_name"].notna()
    & (skill_df["skill_name"].str.strip() != "")
]


# -----------------------------
# Title
# -----------------------------

st.title("🔍 Market Explorer")


# -----------------------------
# Filters
# -----------------------------

col1, col2, col3 = st.columns(3)


with col1:
    skill_options = [
        "All"
    ] + sorted(
        skill_df["skill_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_skill = st.selectbox(
        "Select Skill",
        skill_options
    )


with col2:
    category_options = [
        "All"
    ] + sorted(
        skill_df["skill_category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.selectbox(
        "Select Category",
        category_options
    )


with col3:
    type_options = [
        "All"
    ] + sorted(
        skill_df["skill_type"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_type = st.selectbox(
        "Select Skill Type",
        type_options
    )


filtered = skill_df.copy()


if selected_skill != "All":
    filtered = filtered[
        filtered["skill_name"] == selected_skill
    ]


if selected_category != "All":
    filtered = filtered[
        filtered["skill_category"] == selected_category
    ]


if selected_type != "All":
    filtered = filtered[
        filtered["skill_type"] == selected_type
    ]


# -----------------------------
# KPI Cards
# -----------------------------

c1, c2, c3 = st.columns(3)


with c1:
    st.metric(
        "Skills Found",
        f"{filtered['skill_name'].nunique():,}"
    )


with c2:
    st.metric(
        "Total Demand",
        f"{filtered['occurrences'].sum():,}"
    )


with c3:
    st.metric(
        "Median Salary",
        f"£{filtered['median_salary'].median():,.0f}"
    )


st.divider()


# -----------------------------
# Skill Distribution
# -----------------------------

st.subheader("Skill Demand")


skill_chart = (
    filtered
    .sort_values(
        "occurrences",
        ascending=False
    )
    .head(20)
)


fig1 = px.bar(
    skill_chart,
    x="skill_name",
    y="occurrences",
    color="skill_category",
    labels={
        "skill_name": "Skill",
        "occurrences": "Job Demand",
        "skill_category": "Category"
    },
    height=450
)


st.plotly_chart(
    fig1,
    use_container_width=True
)


# -----------------------------
# Company Profile
# -----------------------------

st.divider()

st.subheader("Companies Using Selected Skills")


company_filtered = company_df.copy()


if selected_skill != "All":
    company_filtered = company_filtered[
        company_filtered["skill_name"] == selected_skill
    ]


company_filtered = (
    company_filtered
    .sort_values(
        "occurrences",
        ascending=False
    )
    .head(20)
)


if not company_filtered.empty:

    fig2 = px.bar(
        company_filtered,
        x="company_name",
        y="occurrences",
        labels={
            "company_name": "Company",
            "occurrences": "Job Count"
        },
        height=450
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# -----------------------------
# UK Job Market Map
# -----------------------------

st.divider()

st.subheader("📍 UK Job Market Map")

from utils.geo_cache import save_coordinates


location_filtered = location_df.copy()

location_filtered = add_coordinates(
    location_filtered
)


if (
    "latitude" in location_filtered.columns
    and
    "longitude" in location_filtered.columns
):

    save_coordinates(
        location_filtered[
            [
                "location",
                "latitude",
                "longitude"
            ]
        ]
    )

if selected_skill != "All":
    location_filtered = location_filtered[
        location_filtered["skill_name"] == selected_skill
    ]


location_filtered = add_coordinates(
    location_filtered
)


map_df = location_filtered.dropna(
    subset=[
        "latitude",
        "longitude"
    ]
)


if not map_df.empty:

    fig3 = px.scatter_mapbox(
        map_df,
        lat="latitude",
        lon="longitude",
        size="demand",
        color="median_salary",
        hover_name="location",
        hover_data={
            "skill_name": True,
            "skill_category": True,
            "skill_type": True,
            "demand": True,
            "median_salary": ":,.0f",
            "latitude": False,
            "longitude": False
        },
        zoom=5,
        height=650
    )


    fig3.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={
            "lat": 54.5,
            "lon": -3
        },
        margin={
            "r":0,
            "t":0,
            "l":0,
            "b":0
        }
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )


else:

    st.info(
        "No mapped locations available for selected filters."
    )