import streamlit as st
import pandas as pd

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

from src.database.connection import engine
from utils.ui import page_header, format_salary

st.title("AI Pipeline & Data Quality")

page_header(
    "UK Labour Market Overview",
    "AI-powered analysis of UK job demand, skills and salary trends."
)

query = """
SELECT *
FROM vw_pipeline_metrics
"""


df = pd.read_sql(
    query,
    engine
)


data = df.iloc[0]


# KPI Cards

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Jobs Processed",
    f"{data['total_jobs_processed']:,}"
)


col2.metric(
    "Skills Extracted",
    f"{data['total_skills_extracted']:,}"
)


col3.metric(
    "Skills with Taxonomy Mapping",
    f"{data['mapped_skills']:,}"
)


col4.metric(
    "Taxonomy Coverage",
    f"{data['taxonomy_coverage']:.2%}"
)



st.divider()


# Refresh Information

st.subheader(
    "Pipeline Refresh"
)


col5, col6 = st.columns(2)


col5.info(
    f"Last Job Refresh: {data['last_job_refresh']}"
)


col6.info(
    f"Last Skill Refresh: {data['last_skill_refresh']}"
)



# Data Quality Summary

st.subheader(
    "Pipeline Status"
)


quality_df = pd.DataFrame(
    {
        "Metric": [
            "Jobs Loaded",
            "Skills Extracted",
            "Skill Mapping Coverage"
        ],
        "Value": [
            data["total_jobs_processed"],
            data["total_skills_extracted"],
            data["taxonomy_coverage"]
        ]
    }
)


st.dataframe(
    quality_df,
    hide_index=True
)