import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

from src.database.connection import engine
from utils.ui import page_header, format_salary


page_header(
    "UK Labour Market Overview",
    "AI-powered analysis of UK job demand, skills and salary trends."
)

query = """
SELECT *
FROM vw_market_overview
"""


df = pd.read_sql(
    query,
    engine
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Jobs",
    f"{df['total_jobs'][0]:,}"
)

col2.metric(
    "Companies",
    f"{df['total_companies'][0]:,}"
)

col3.metric(
    "Locations",
    f"{df['total_locations'][0]:,}"
)

col4.metric(
    "Average Salary",
    f"£{df['average_salary'][0]:,.0f}"
)


# 1) Load data from Neon

map_df = pd.read_sql(
    """
    SELECT *
    FROM vw_jobs_map
    """,
    engine
)


# 2) Create circle size based on job demand

map_df["radius"] = (
    np.sqrt(map_df["job_count"])
    * 2000
)


# 3) Format salary for tooltip

map_df["salary_display"] = (
    map_df["average_salary"]
    .apply(
        lambda x: f"£{x:,.2f}"
    )
)


# 4) Create colour based on salary

min_salary = map_df["average_salary"].min()
max_salary = map_df["average_salary"].max()


def salary_colour(value):

    ratio = (
        value - min_salary
    ) / (
        max_salary - min_salary
    )

    return [
        int(255 * (1 - ratio)),
        100,
        int(255 * ratio),
        180
    ]


map_df["colour"] = (
    map_df["average_salary"]
    .apply(salary_colour)
)


# 5) Create map layer

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position=[
        "longitude",
        "latitude"
    ],
    get_radius="radius",
    get_fill_color="colour",
    pickable=True
)


# 6) Map view

view = pdk.ViewState(
    latitude=54.5,
    longitude=-2.5,
    zoom=5
)


# 7) Display map

st.subheader(
    "UK Job Market Map"
)


st.pydeck_chart(
    pdk.Deck(
        layers=[
            layer
        ],
        initial_view_state=view,
        tooltip={
            "text":
            "{city}\n"
            "Jobs: {job_count}\n"
            "Average Salary: {salary_display}"
        }
    )
)