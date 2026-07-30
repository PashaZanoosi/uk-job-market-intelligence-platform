# UK Job Market Intelligence Platform

An end-to-end UK job market analytics platform that collects, processes, enriches, and analyses job market data using Python, SQL, AI, Power BI, and Streamlit.

The project transforms raw job listings into actionable insights about job demand, skills, salaries, locations, companies, and market trends.

## Business Problem

Job market data is large, unstructured, and constantly changing. Job descriptions contain inconsistent titles, locations, salary formats, and skill requirements, making analysis difficult.

This project solves this by building an automated analytics pipeline that converts raw job data into structured business intelligence.

## Solution Overview

The platform workflow:

```
Adzuna API
      ↓
Python Data Collection Pipeline
      ↓
PostgreSQL Database (Neon)
      ↓
AI Skill Extraction \& Classification
      ↓
Analytics Data Layer
      ↓
Power BI Dashboard + Streamlit Application
```

## Key Features

### Data Engineering

* Automated job data collection from Adzuna API
* Data cleaning and transformation pipeline
* PostgreSQL database modelling
* Snapshot-based historical tracking

### AI-Powered Analysis

* AI extraction of skills from job descriptions
* Skill categorisation using LLM models
* Automated market insight generation
* Skill demand analysis

### Business Intelligence

Interactive dashboards covering:

* Job demand by location
* Salary analysis
* Skill popularity and trends
* Market insights
* Job pipeline performance

## Technology Stack

### Data \& Analytics

* Python
* SQL
* PostgreSQL
* Pandas
* SQLAlchemy

### AI

* Groq API
* LLM-based skill extraction
* Automated insight generation

### Visualisation

* Power BI
* Streamlit
* PyDeck

### Data Source

* Adzuna Job Search API

## Project Structure

```
uk-job-market-intelligence/
│
├── app/
│   ├── pages/
│   └── utils/
│
├── src/
│   ├── ai/
│   ├── analytics/
│   ├── data/
│   ├── database/
│   └── utils/
│
├── sql/
│
├── powerbi/
│
├── run\_pipeline.py
│
└── README.md
```

## Outputs

The platform delivers:

* Interactive Streamlit analytics application
* Power BI executive dashboard
* AI-generated market reports
* Structured job and skill intelligence database

## Business Value

This project demonstrates how data engineering, AI automation, and business intelligence can be combined to create a repeatable decision-support system for labour market analysis.

## Future Improvements

* Real-time job market monitoring
* Automated dashboard refresh
* Improved skill taxonomy coverage
* Advanced forecasting models
* Cloud deployment

