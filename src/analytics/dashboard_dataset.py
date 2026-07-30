from src.database.connection import engine
from dotenv import load_dotenv
import os
import pandas as pd


# ==========================
# Environment
# ==========================

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

OUTPUT_DIR = "data/dashboard"

# ==========================
# Create folder
# ==========================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)



# ==========================
# Skill Demand Dataset
# ==========================

def export_skill_demand():

    query = """

    SELECT

        s.skill_name,
        s.category,
        st.name AS taxonomy,
        COUNT(DISTINCT js.job_id)
        AS job_count


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

    """


    df = pd.read_sql(
        query,
        engine
    )


    df.to_csv(
        f"{OUTPUT_DIR}/skill_demand.csv",
        index=False
    )


    print(
        "skill_demand.csv created"
    )




# ==========================
# Taxonomy Dataset
# ==========================

def export_taxonomy_demand():

    query = """

    SELECT

        st.name AS taxonomy,

        COUNT(
            DISTINCT js.job_id
        ) AS jobs,


        COUNT(
            DISTINCT s.skill_id
        ) AS skills


    FROM skills s


    JOIN skill_taxonomy st
    ON s.taxonomy_id = st.taxonomy_id


    JOIN job_skills js
    ON s.skill_id = js.skill_id


    WHERE st.level = 2


    GROUP BY st.name


    ORDER BY jobs DESC

    """



    df = pd.read_sql(
        query,
        engine
    )


    df.to_csv(
        f"{OUTPUT_DIR}/taxonomy_demand.csv",
        index=False
    )


    print(
        "taxonomy_demand.csv created"
    )




# ==========================
# Category Dataset
# ==========================

def export_category_demand():

    query = """

    SELECT

        s.category,


        COUNT(
            DISTINCT js.job_id
        ) AS jobs,


        COUNT(
            DISTINCT s.skill_id
        ) AS skills


    FROM skills s


    JOIN job_skills js
    ON s.skill_id = js.skill_id


    GROUP BY s.category


    ORDER BY jobs DESC

    """



    df = pd.read_sql(
        query,
        engine
    )


    df.to_csv(
        f"{OUTPUT_DIR}/category_demand.csv",
        index=False
    )


    print(
        "category_demand.csv created"
    )




# ==========================
# Job Skill Matrix
# ==========================

def export_job_skill_matrix():

    query = """

    SELECT


        js.job_id,

        s.skill_name,

        s.category,

        st.name AS taxonomy,


        js.confidence_score



    FROM job_skills js


    JOIN skills s

    ON js.skill_id = s.skill_id


    JOIN skill_taxonomy st

    ON s.taxonomy_id = st.taxonomy_id



    """



    df = pd.read_sql(
        query,
        engine
    )


    df.to_csv(
        f"{OUTPUT_DIR}/job_skill_matrix.csv",
        index=False
    )


    print(
        "job_skill_matrix.csv created"
    )




# ==========================
# Skill Tree
# ==========================

def export_skill_tree():

    query = """

    SELECT


        s.skill_name,


        s.category,


        st.name AS taxonomy,


        st.parent_id



    FROM skills s


    JOIN skill_taxonomy st

    ON s.taxonomy_id = st.taxonomy_id



    """



    df = pd.read_sql(
        query,
        engine
    )


    df.to_csv(
        f"{OUTPUT_DIR}/skill_tree.csv",
        index=False
    )


    print(
        "skill_tree.csv created"
    )




# ==========================
# Run
# ==========================


print("==============================")
print("BUILDING DASHBOARD DATASETS")
print("==============================")


export_skill_demand()

export_taxonomy_demand()

export_category_demand()

export_job_skill_matrix()

export_skill_tree()



print()

print(
    "Dashboard datasets ready"
)