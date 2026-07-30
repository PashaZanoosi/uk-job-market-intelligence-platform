import os
import json
import glob
from dotenv import load_dotenv

from sqlalchemy import text
from src.database.connection import engine


# ==========================
# Environment
# ==========================

load_dotenv()

# ==========================
# Find latest clean file
# ==========================

files = glob.glob(
    "data/processed/jobs_*_clean.json"
)


if not files:
    raise Exception(
        "No clean job file found"
    )


latest_file = max(
    files,
    key=os.path.getmtime
)



# ==========================
# Load JSON
# ==========================

with open(
    latest_file,
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)



jobs = data.get(
    "jobs",
    []
)



print("==============================")
print("START DATABASE LOAD")
print("==============================")


print(
    "Source:",
    latest_file
)


print(
    "Jobs found:",
    len(jobs)
)



# ==========================
# Insert Jobs
# ==========================

inserted = 0
skipped = 0
errors = 0



with engine.begin() as connection:


    for job in jobs:


        try:


            existing = connection.execute(

                text("""
                    SELECT job_id
                    FROM jobs
                    WHERE job_id = :job_id
                """),

                {
                    "job_id":
                        job["job_id"]
                }

            ).fetchone()



            if existing:

                skipped += 1

                continue



            salary_min = job.get(
                "salary_min"
            )

            salary_max = job.get(
                "salary_max"
            )


            average_salary = None


            if (
                salary_min is not None
                and
                salary_max is not None
            ):

                average_salary = int(
                    (salary_min + salary_max ) / 2 )

            connection.execute(

                text("""
                    INSERT INTO jobs
                    (
                        job_id,
                        title,
                        company,
                        location,
                        category,
                        salary_min,
                        salary_max,
                        average_salary,
                        created_date,
                        description
                    )

                    VALUES
                    (
                        :job_id,
                        :title,
                        :company,
                        :location,
                        :category,
                        :salary_min,
                        :salary_max,
                        :average_salary,
                        :created_date,
                        :description
                    )
                """),

                {

                    "job_id":
                        job.get("job_id"),

                    "title":
                        job.get("title"),

                    "company":
                        job.get("company"),

                    "location":
                        job.get("location"),

                    "category":
                        job.get("category"),

                    "salary_min":
                        salary_min,

                    "salary_max":
                        salary_max,

                    "average_salary":
                        average_salary,

                    "created_date":
                        job.get("created"),

                    "description":
                        job.get("description")

                }

            )


            inserted += 1



        except Exception as e:


            errors += 1


            print(
                "Error:",
                job.get("job_id"),
                e
            )



# ==========================
# Results
# ==========================

print()

print("==============================")
print("LOAD RESULTS")
print("==============================")


print(
    "Inserted:",
    inserted
)


print(
    "Skipped:",
    skipped
)


print(
    "Errors:",
    errors
)


print(
    "Snapshots handled by: create_snapshots.py"
)


print("==============================")
print("Finished")