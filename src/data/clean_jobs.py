import json
import os
import glob

from datetime import datetime

# ==========================
# Find latest raw file
# ==========================

files = glob.glob(
    "data/raw/jobs_*.json"
)

if not files:
    raise Exception(
        "No raw job files found"
    )

latest_file = max(
    files,
    key=os.path.getmtime
)

# ==========================
# Load raw data
# ==========================

with open(
    latest_file,
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)

jobs = (
    data.get("results")
    or data.get("jobs")
    or []
)

print("==============================")
print("START CLEAN JOBS")
print("==============================")

print(
    "Input records:",
    len(jobs)
)

# ==========================
# Clean
# ==========================

clean_jobs = []
seen_ids = set()
removed_duplicates = 0
removed_invalid = 0

for job in jobs:


    job_id = job.get(
        "id"
    )

    title = job.get(
        "title"
    )

    if not job_id or not title:

        removed_invalid += 1

        continue

    if job_id in seen_ids:

        removed_duplicates += 1

        continue

    seen_ids.add(
        job_id
    )

    company = job.get(
        "company",
        {}
    )

    location = job.get(
        "location",
        {}
    )

    category = job.get(
        "category",
        {}
    )

    clean_job = {

        "job_id": job_id,

        "title": title.strip(),

        "company":
            company.get(
                "display_name",
                "Unknown"
            )
            if isinstance(company, dict)
            else "Unknown",

        "location":
            location.get(
                "display_name",
                "Unknown"
            )
            if isinstance(location, dict)
            else "Unknown",

        "category":
            category.get(
                "label",
                "Unknown"
            )
            if isinstance(category, dict)
            else "Unknown",

        "salary_min":
            job.get(
                "salary_min"
            ),

        "salary_max":
            job.get(
                "salary_max"
            ),

        "salary_is_predicted":
            job.get(
                "salary_is_predicted"
            ),

        "created":
            job.get(
                "created"
            ),

        "description":
            job.get(
                "description",
                ""
            ),

        "redirect_url":
            job.get(
                "redirect_url"
            )

    }

    clean_jobs.append(
        clean_job
    )

# ==========================
# Save
# ==========================

os.makedirs(
    "data/processed",
    exist_ok=True
)

date = datetime.now().strftime(
    "%Y%m%d"
)

output = (
    f"data/processed/"
    f"jobs_{date}_clean.json"
)

result = {

    "clean_date":
        datetime.now().isoformat(),

    "source_file":
        latest_file,

    "total_jobs":
        len(clean_jobs),

    "jobs":
        clean_jobs

}

with open(
    output,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        result,
        file,
        ensure_ascii=False,
        indent=4
    )

print("==============================")
print("CLEAN RESULTS")
print("==============================")

print(
    "Output records:",
    len(clean_jobs)
)

print(
    "Removed duplicates:",
    removed_duplicates
)

print(
    "Removed invalid:",
    removed_invalid
)

print(
    "Saved:",
    output
)

print("==============================")