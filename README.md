# UK Job Market Intelligence Platform

AI-driven job market intelligence platform that automatically collects, processes and analyses UK job market data to provide actionable insights into salaries, skills demand, regional hiring trends and employer activity.

Live dashboard:
https://uk-job-market.streamlit.app/

---

## Overview

This project was built to demonstrate an end-to-end analytics workflow, from automated data collection through ETL pipelines to interactive business intelligence dashboards.

The platform continuously gathers job advertisements, stores them in PostgreSQL, enriches them using AI-assisted skill extraction, and presents insights through an interactive Streamlit application.

---

## Features

- Automated ETL pipeline
- PostgreSQL (Neon) cloud database
- AI-assisted skill extraction
- UK labour market dashboards
- Salary analysis
- Skills demand analysis
- Company insights
- Regional hiring trends
- Interactive maps
- Time-series trend analysis

---

## Technology Stack

Python

SQL

PostgreSQL (Neon)

Streamlit

Power BI

Plotly

GitHub Actions

Git

---

## Dashboard

The dashboard contains several interactive pages.

### Overview

- Job market summary
- Top skills
- Job categories

### Skills

- Most demanded skills
- Salary by skill
- Skills by category

### Explorer

- Regional hiring map
- Job explorer
- Skills explorer

### Network

- Company–skill relationships

### Market Trends

- Time-series analysis
- Skills trends

### Companies

- Company insights
- Hiring activity

---

## Data Pipeline

The project automatically

1. Collects UK job advertisements
2. Cleans and standardises the data
3. Stores structured data in PostgreSQL
4. Extracts skills using AI
5. Updates analytical views
6. Serves dashboards through Streamlit

---

## Project Structure

```text
app/
src/
powerbi/
requirements.txt
requirements-pipeline.txt
README.md
```

---

## Future Improvements

- Demand forecasting using Time Series and Machine Learning
- AI-powered labour market recommendations
- Resume-to-job matching
- Skill gap analysis
- LLM-powered career assistant

---

## Author

Aliakbar Pashazanoosi