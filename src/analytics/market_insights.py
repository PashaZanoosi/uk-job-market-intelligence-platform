from sqlalchemy import text
from src.database.connection import engine
from dotenv import load_dotenv
import os
import json
from datetime import datetime


# ==========================
# Environment
# ==========================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

OUTPUT_FILE = "data/market_insights.json"

# ==========================
# Top Skills
# ==========================

def get_skill_demand():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
            SELECT
                s.skill_name,
                s.category,
                st.name AS taxonomy,
                COUNT(DISTINCT js.job_id) AS job_count

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

            ORDER BY job_count DESC
            """)
        )

        return result.fetchall()



# ==========================
# Taxonomy Demand
# ==========================

def get_taxonomy_demand():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
            SELECT

                st.name AS taxonomy,

                COUNT(DISTINCT js.job_id)
                AS jobs,

                COUNT(DISTINCT s.skill_id)
                AS skills


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
# Build Insights
# ==========================

def build_insights():


    skills = get_skill_demand()

    taxonomy = get_taxonomy_demand()



    insights = {

        "generated_at":
            datetime.now().isoformat(),


        "top_skills": [],


        "taxonomy_demand": [],


        "summary": {}

    }



    # ----------------------
    # Top skills
    # ----------------------

    for row in skills[:20]:

        insights["top_skills"].append({

            "skill":
                row.skill_name,

            "category":
                row.category,

            "taxonomy":
                row.taxonomy,

            "job_demand":
                row.job_count

        })



    # ----------------------
    # Taxonomy
    # ----------------------

    for row in taxonomy:

        insights["taxonomy_demand"].append({

            "taxonomy":
                row.taxonomy,

            "jobs":
                row.jobs,

            "skills":
                row.skills

        })



    # ----------------------
    # Summary Metrics
    # ----------------------

    insights["summary"] = {


        "total_skills":
            len(skills),


        "total_taxonomies":
            len(taxonomy),


        "highest_demand_skill":

            skills[0].skill_name
            if skills
            else None,


        "highest_demand_taxonomy":

            taxonomy[0].taxonomy
            if taxonomy
            else None

    }



    return insights



# ==========================
# Save JSON
# ==========================

def save_json(data):

    os.makedirs(
        "data",
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )



# ==========================
# Run
# ==========================


print("==============================")
print("BUILDING MARKET INSIGHTS")
print("==============================")


insights = build_insights()


save_json(insights)


print()

print(
    "Top Skill:",
    insights["summary"]["highest_demand_skill"]
)


print(
    "Top Taxonomy:",
    insights["summary"]["highest_demand_taxonomy"]
)


print()

print(
    "Saved:",
    OUTPUT_FILE
)


print()

print("Finished")