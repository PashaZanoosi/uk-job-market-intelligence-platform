from dotenv import load_dotenv
from sqlalchemy import text
from src.database.connection import engine
import os


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

def top_skills_by_jobs(limit=20):

    print("\n==============================")
    print("TOP SKILLS BY JOB DEMAND")
    print("==============================")


    with engine.connect() as connection:

        result = connection.execute(

            text("""
            SELECT
                s.skill_name,
                s.category,
                COUNT(DISTINCT js.job_id) AS job_count

            FROM skills s

            JOIN job_skills js
                ON s.skill_id = js.skill_id

            GROUP BY
                s.skill_name,
                s.category

            ORDER BY job_count DESC

            LIMIT :limit
            """),

            {
                "limit": limit
            }
        )


        for row in result:

            print(
                f"{row.skill_name:<40} | "
                f"{row.category:<15} | "
                f"{row.job_count} jobs"
            )





def skills_by_category():

    print("\n==============================")
    print("SKILLS BY CATEGORY")
    print("==============================")


    with engine.connect() as connection:

        result = connection.execute(

            text("""
            SELECT
                category,
                COUNT(skill_id) AS skill_count

            FROM skills

            GROUP BY category

            ORDER BY skill_count DESC
            """)
        )


        for row in result:

            print(
                f"{row.category:<20} "
                f"{row.skill_count}"
            )





def taxonomy_job_demand():

    print("\n==============================")
    print("TAXONOMY JOB DEMAND")
    print("==============================")


    with engine.connect() as connection:


        result = connection.execute(

            text("""
            SELECT

                st.name AS taxonomy,

                COUNT(DISTINCT js.job_id)
                AS job_count,

                COUNT(s.skill_id)
                AS skill_count


            FROM skills s


            JOIN skill_taxonomy st

                ON s.taxonomy_id = st.taxonomy_id


            JOIN job_skills js

                ON s.skill_id = js.skill_id


            GROUP BY st.name


            ORDER BY job_count DESC

            """)
        )


        for row in result:


            print(

                f"{row.taxonomy:<35} | "
                f"Jobs: {row.job_count:<5} | "
                f"Skills: {row.skill_count}"

            )





def category_job_matrix():


    print("\n==============================")
    print("CATEGORY JOB MATRIX")
    print("==============================")


    with engine.connect() as connection:


        result = connection.execute(

            text("""
            SELECT

                s.category,

                COUNT(DISTINCT js.job_id)
                AS jobs,

                COUNT(DISTINCT s.skill_id)
                AS skills


            FROM skills s


            JOIN job_skills js

                ON s.skill_id = js.skill_id


            GROUP BY s.category


            ORDER BY jobs DESC

            """)
        )


        for row in result:

            print(

                f"{row.category:<20} | "
                f"Jobs: {row.jobs:<5} | "
                f"Skills: {row.skills}"

            )





def export_market_dataset():


    print("\n==============================")
    print("MARKET DATASET")
    print("==============================")


    with engine.connect() as connection:


        result = connection.execute(

            text("""
            SELECT

                s.skill_name,

                s.category,

                st.name AS taxonomy,

                COUNT(DISTINCT js.job_id)
                AS demand


            FROM skills s


            LEFT JOIN skill_taxonomy st

                ON s.taxonomy_id = st.taxonomy_id


            LEFT JOIN job_skills js

                ON s.skill_id = js.skill_id


            GROUP BY

                s.skill_name,
                s.category,
                st.name


            ORDER BY demand DESC

            """)
        )


        for row in result.fetchmany(30):

            print(

                f"{row.skill_name:<35} | "
                f"{row.category:<15} | "
                f"{row.taxonomy:<30} | "
                f"{row.demand}"

            )





if __name__ == "__main__":


    top_skills_by_jobs()


    skills_by_category()


    taxonomy_job_demand()


    category_job_matrix()


    export_market_dataset()