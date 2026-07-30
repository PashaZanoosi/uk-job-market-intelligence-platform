CREATE VIEW vw_jobs_by_location AS

SELECT
    location,
    COUNT(*) AS total_jobs

FROM jobs

GROUP BY location

ORDER BY total_jobs DESC;


CREATE VIEW vw_salary_analysis AS

SELECT
    title,
    COUNT(*) AS job_count,
    ROUND(AVG(average_salary),0) AS average_salary

FROM jobs

WHERE average_salary IS NOT NULL

GROUP BY title

ORDER BY average_salary DESC;

CREATE VIEW vw_top_hiring_companies AS

SELECT
    company,
    COUNT(*) AS vacancies

FROM jobs

GROUP BY company

ORDER BY vacancies DESC
LIMIT 20;