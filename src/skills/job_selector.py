# =====================================================
# job_selector.py
# Select and reserve jobs waiting for skill extraction
# =====================================================

from sqlalchemy import text

from src.database.connection import engine


def get_pending_jobs(limit=10):

    sql = text("""
        WITH selected_jobs AS (

            SELECT job_id

            FROM jobs

            WHERE skills_extraction_status = 'pending'
            AND (
                description IS NOT NULL
                OR redirect_url IS NOT NULL
            )

            ORDER BY first_seen_date ASC

            LIMIT :limit

            FOR UPDATE SKIP LOCKED

        )

        UPDATE jobs

        SET
            skills_extraction_status = 'processing'

        WHERE job_id IN (
            SELECT job_id
            FROM selected_jobs
        )

        RETURNING
            job_id,
            title,
            redirect_url,
            description,
            skills_extraction_status
    """)


    with engine.begin() as connection:

        result = connection.execute(
            sql,
            {
                "limit": limit
            }
        )

        jobs = result.fetchall()


    return jobs