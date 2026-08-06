TOP_SKILLS_QUERY = """
SELECT *
FROM vw_skill_market_value
ORDER BY demand DESC;
"""

JOB_CATEGORY_QUERY = """
SELECT *
FROM vw_job_category_overview
ORDER BY job_count DESC;
"""

OVERVIEW_SKILL_STATS_QUERY = """
SELECT
    COUNT(*) AS total_skills,
    MAX(skill_name) FILTER (
        WHERE demand = (SELECT MAX(demand) FROM vw_skill_market_value)
    ) AS top_skill,
    MAX(demand) AS highest_demand,
    ROUND(
        PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY median_salary)::numeric,
        0
    ) AS median_skill_salary
FROM vw_skill_market_value;
"""

OVERVIEW_CATEGORY_STATS_QUERY = """
SELECT
    COUNT(*) AS total_categories
FROM vw_job_category_overview;
"""

SKILL_MARKET_VALUE_QUERY = """
SELECT *
FROM vw_skill_market_value
ORDER BY demand DESC;
"""

SKILL_SALARY_RANGE_QUERY = """
SELECT *
FROM vw_skill_salary_range
ORDER BY salary_median DESC;
"""

SKILL_CATEGORY_QUERY = """
SELECT *
FROM vw_skill_category_salary
ORDER BY occurrences DESC;
"""

COMPANY_SKILL_PROFILE_QUERY = """
SELECT *
FROM vw_company_skill_profile
ORDER BY occurrences DESC;
"""

LOCATION_SKILL_SALARY_QUERY = """
SELECT *
FROM vw_location_skill_salary
ORDER BY median_salary DESC;
"""

SKILL_COOCCURRENCE_QUERY = """
SELECT *
FROM vw_skill_cooccurrence
ORDER BY cooccurrence_count DESC;
"""

FORECASTING_MARKET_TREND_QUERY = """
SELECT *
FROM vw_forecasting_market_trend
ORDER BY date;
"""

COMPANY_SKILL_PROFILE_QUERY = """
SELECT *
FROM vw_company_skill_profile;
"""



