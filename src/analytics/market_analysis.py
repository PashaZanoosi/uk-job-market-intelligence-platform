from sqlalchemy import text
from src.database.connection import engine

from dotenv import load_dotenv
import os


# ==========================
# Environment
# ==========================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ==========================
# TOP SKILLS BY JOB DEMAND
# ==========================

def get_top_skills(limit=20):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
            SELECT
                s.skill_name,
                s.category,
                st.name AS taxonomy,
                COUNT(DISTINCT js.job_id) AS demand

            FROM skills s

            JOIN skill_taxonomy st
            ON s.taxonomy_id = st.taxonomy_id

            JOIN job_skills js
            ON s.skill_id = js.skill_id

            WHERE st.level = 2

            GROUP BY
                s.skill_name,
                s.category,
                st.name

            ORDER BY demand DESC

            LIMIT :limit
            """),
            {
                "limit": limit
            }
        )

        return result.fetchall()



# ==========================
# SKILL CATEGORY DEMAND
# ==========================

def get_category_demand():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
            SELECT
                s.category,
                COUNT(DISTINCT js.job_id) AS jobs,
                COUNT(DISTINCT s.skill_id) AS skills

            FROM skills s

            JOIN job_skills js
            ON s.skill_id = js.skill_id

            GROUP BY s.category

            ORDER BY jobs DESC
            """)
        )

        return result.fetchall()



# ==========================
# TAXONOMY DEMAND
# ==========================

def get_taxonomy_demand():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
            SELECT
                st.name,
                COUNT(DISTINCT js.job_id) AS jobs,
                COUNT(DISTINCT s.skill_id) AS skills

            FROM skills s

            JOIN skill_taxonomy st
            ON s.taxonomy_id = st.taxonomy_id

            JOIN job_skills js
            ON s.skill_id = js.skill_id

            WHERE st.level = 2

            GROUP BY st.name

            ORDER BY jobs DESC
            """)
        )

        return result.fetchall()



# ==========================
# JOB PROFILE
# ==========================

def get_job_profile(job_id):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
            SELECT
                s.skill_name,
                s.category,
                st.name AS taxonomy

            FROM job_skills js

            JOIN skills s
            ON js.skill_id = s.skill_id

            JOIN skill_taxonomy st
            ON s.taxonomy_id = st.taxonomy_id

            WHERE js.job_id = :job_id

            ORDER BY s.skill_name
            """),
            {
                "job_id": job_id
            }
        )

        return result.fetchall()



# ==========================
# TAXONOMY SKILL TREE
# ==========================

def get_taxonomy_tree():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
            SELECT
                st.name AS taxonomy,
                s.skill_name

            FROM skills s

            JOIN skill_taxonomy st
            ON s.taxonomy_id = st.taxonomy_id

            WHERE st.level = 2

            ORDER BY
                st.name,
                s.skill_name
            """)
        )

        return result.fetchall()



# ==========================
# PRINT REPORT
# ==========================

print("\n==============================")
print("TOP SKILLS BY JOB DEMAND")
print("==============================")

for row in get_top_skills():

    print(
        f"{row.skill_name:<35} | "
        f"{row.category:<15} | "
        f"{row.taxonomy:<30} | "
        f"{row.demand} jobs"
    )



print("\n==============================")
print("SKILLS BY CATEGORY")
print("==============================")

for row in get_category_demand():

    print(
        f"{row.category:<20} | "
        f"Jobs: {row.jobs:<5} | "
        f"Skills: {row.skills}"
    )



print("\n==============================")
print("TAXONOMY JOB DEMAND")
print("==============================")

for row in get_taxonomy_demand():

    print(
        f"{row.name:<35} | "
        f"Jobs: {row.jobs:<5} | "
        f"Skills: {row.skills}"
    )



print("\n==============================")
print("JOB PROFILE: 5804007899")
print("==============================")

for row in get_job_profile("5804007899"):

    print(
        f"{row.skill_name:<35} | "
        f"{row.category:<15} | "
        f"{row.taxonomy}"
    )



print("\n==============================")
print("TAXONOMY SKILL TREE")
print("==============================")


current_taxonomy = None


for row in get_taxonomy_tree():

    if current_taxonomy != row.taxonomy:

        current_taxonomy = row.taxonomy

        print("\n")
        print(current_taxonomy)


    print(
        f"  - {row.skill_name}"
    )


print("\nFinished")