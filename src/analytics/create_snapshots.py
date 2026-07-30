from sqlalchemy import text
from src.database.connection import engine
from dotenv import load_dotenv
import os
from datetime import date


# ==========================
# Environment
# ==========================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

TODAY = date.today()

# ==========================
# Skill Demand Snapshot
# ==========================

def create_skill_snapshot():

    with engine.begin() as connection:


        result = connection.execute(
            text("""
                SELECT

                    s.skill_id,

                    COUNT(DISTINCT js.job_id)
                    AS job_count


                FROM skills s


                JOIN job_skills js

                ON s.skill_id = js.skill_id


                GROUP BY s.skill_id

            """)
        )


        rows = result.fetchall()



        for row in rows:


            connection.execute(

                text("""
                    INSERT INTO skill_demand_snapshots
                    (
                        snapshot_date,
                        skill_id,
                        job_count
                    )

                    VALUES
                    (
                        :snapshot_date,
                        :skill_id,
                        :job_count
                    )


                    ON CONFLICT
                    (
                        snapshot_date,
                        skill_id
                    )


                    DO UPDATE SET

                    job_count = EXCLUDED.job_count

                """),

                {
                    "snapshot_date": TODAY,
                    "skill_id": row.skill_id,
                    "job_count": row.job_count
                }

            )


    print(
        f"Skill snapshot created: {len(rows)} records"
    )





# ==========================
# Taxonomy Demand Snapshot
# ==========================

def create_taxonomy_snapshot():

    with engine.begin() as connection:


        result = connection.execute(

            text("""
                SELECT

                    st.taxonomy_id,


                    COUNT(DISTINCT js.job_id)
                    AS job_count,


                    COUNT(DISTINCT s.skill_id)
                    AS skill_count



                FROM skills s


                JOIN skill_taxonomy st

                ON s.taxonomy_id = st.taxonomy_id


                JOIN job_skills js

                ON s.skill_id = js.skill_id



                WHERE st.level = 2



                GROUP BY st.taxonomy_id

            """)

        )


        rows = result.fetchall()



        for row in rows:


            connection.execute(

                text("""
                    INSERT INTO taxonomy_demand_snapshots
                    (
                        snapshot_date,
                        taxonomy_id,
                        job_count,
                        skill_count
                    )


                    VALUES
                    (
                        :snapshot_date,
                        :taxonomy_id,
                        :job_count,
                        :skill_count
                    )


                    ON CONFLICT
                    (
                        snapshot_date,
                        taxonomy_id
                    )


                    DO UPDATE SET

                    job_count = EXCLUDED.job_count,

                    skill_count = EXCLUDED.skill_count

                """),

                {
                    "snapshot_date": TODAY,
                    "taxonomy_id": row.taxonomy_id,
                    "job_count": row.job_count,
                    "skill_count": row.skill_count
                }

            )


    print(
        f"Taxonomy snapshot created: {len(rows)} records"
    )





# ==========================
# Validation
# ==========================

def check_snapshot_counts():

    with engine.connect() as connection:


        skill_count = connection.execute(

            text("""
                SELECT COUNT(*)

                FROM skill_demand_snapshots

                WHERE snapshot_date = :today

            """),

            {
                "today": TODAY
            }

        ).scalar()



        taxonomy_count = connection.execute(

            text("""
                SELECT COUNT(*)

                FROM taxonomy_demand_snapshots

                WHERE snapshot_date = :today

            """),

            {
                "today": TODAY
            }

        ).scalar()



    print()

    print(
        f"Today's skill snapshots: {skill_count}"
    )

    print(
        f"Today's taxonomy snapshots: {taxonomy_count}"
    )





# ==========================
# Run
# ==========================

print("==============================")
print("CREATING MARKET SNAPSHOTS")
print("==============================")


create_skill_snapshot()

create_taxonomy_snapshot()


check_snapshot_counts()


print()

print(
    "Snapshot date:",
    TODAY
)


print()

print("Finished")