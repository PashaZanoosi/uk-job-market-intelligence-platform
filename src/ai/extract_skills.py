# =====================================================
# extract_skills.py
# AI Batch Skill Extraction Pipeline
# =====================================================

import os
import json
import time
import hashlib

from datetime import datetime, date
from dotenv import load_dotenv
from groq import Groq
from sqlalchemy import text
from src.database.connection import engine
from src.utils.telegram_alert import send_message

# =====================================================
# Environment
# =====================================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================================
# Configuration
# =====================================================

MODEL_NAME = "llama-3.1-8b-instant"
BATCH_SIZE = 15
MAX_DESCRIPTION_LENGTH = 1200
MAX_RETRIES = 3
RETRY_DELAYS = [
    60,
    120,
    180
]

TEMPERATURE = 0

# =====================================================
# Helper Functions
# =====================================================

def create_hash(value):

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()

def clean_json_response(content):
    """
    Remove accidental markdown
    """
    content = content.strip()

    if content.startswith("```"):

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    return content

def chunk_list(items, size):

    for i in range(
        0,
        len(items),
        size
    ):

        yield items[i:i + size]

def safe_float(value):
    try:
        return float(value)
    except:
        return 0.5

# =====================================================
# Database Checks
# =====================================================

def job_already_processed(job_id):
    with engine.connect() as connection:
        result = connection.execute(

            text("""
                SELECT COUNT(*)

                FROM job_skills

                WHERE job_id = :job_id

            """),

            {
                "job_id": job_id
            }

        )


        return result.scalar() > 0


def get_jobs_for_processing(limit=500):

    with engine.connect() as connection:

        result = connection.execute(

            text("""
                SELECT

                    job_id,
                    title,
                    description

                FROM jobs

                WHERE description IS NOT NULL

                AND LENGTH(description) > 200

                AND NOT EXISTS

                (

                    SELECT 1

                    FROM job_skills js

                    WHERE js.job_id = jobs.job_id

                )

                LIMIT :limit

            """),

            {
                "limit": limit
            }

        )

        return result.fetchall()

# ==========================
# AI Extraction Batch
# ==========================

def extract_skills_batch(
    jobs
):
    job_text = ""

    for job in jobs:

        description = (

            job.description

            or ""

        )

        job_text += f"""

JOB_ID:
{job.job_id}

DESCRIPTION:
{description[:MAX_DESCRIPTION_LENGTH]}

---------------------

"""


    system_prompt = """

You are extracting professional skills
from UK job descriptions.

For each job:

Return only skills explicitly required
or clearly mentioned.

Rules:

- Extract 2 to 5 skills per job.
- Use standard professional skill names.
- Avoid generic phrases.
- Do not infer skills from job title only.

Use one of these categories:

Technical
Business
Methodology
Domain
Soft Skill

Confidence:
1.0 = explicitly mentioned
0.7 = strongly implied
0.5 = weakly implied

Return JSON only.
Format:
{
    "jobs": [
        {
            "job_id": "123",
            "skills": [
                {
                    "name": "Skill",
                    "category": "Technical",
                    "confidence": 0.9
                }
            ]
        }
    ]
}

Do not return markdown.
Do not add explanations.

"""
    print(
        "Sending batch to Groq...",
        flush=True
    )

    request_start = datetime.now()
    response = (
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": job_text
                }
            ],

            temperature=TEMPERATURE,

            response_format={
                "type": "json_object"
            }
        )
    )

    request_duration = (
        datetime.now()

        -

        request_start
    )

    print(
        "Groq response received.",
        flush=True
    )

    print(

        f"Groq request time: "
        f"{request_duration}",

        flush=True

    )


    content = (

        response

        .choices[0]

        .message

        .content

    )


    return json.loads(

        clean_json_response(

            content

        )

    )




# ==========================
# Save Extracted Skills
# ==========================

def process_batch_results(results):


    processed = 0


    for item in results.get(
        "results",
        []
    ):


        job_id = item.get(
            "job_id"
        )


        skills = item.get(
            "skills",
            []
        )


        for skill in skills:


            skill_id = get_or_create_skill(

                skill["name"],

                skill["category"]

            )


            save_job_skill(

                job_id,

                skill_id,

                skill.get(
                    "confidence",
                    0.5
                )

            )


        processed += 1


    return processed

# ==========================
# Database Skill Management
# ==========================

def get_or_create_skill(
    skill_name,
    category
):

    with engine.begin() as connection:

        result = connection.execute(

            text("""
                SELECT
                    skill_id

                FROM skills

                WHERE LOWER(skill_name)
                =
                LOWER(:skill_name)

            """),

            {
                "skill_name": skill_name
            }

        )


        existing = result.fetchone()


        if existing:

            return existing[0]



        result = connection.execute(

            text("""
                INSERT INTO skills
                (
                    skill_name,
                    category
                )

                VALUES
                (
                    :skill_name,
                    :category
                )

                RETURNING skill_id

            """),

            {
                "skill_name": skill_name,
                "category": category
            }

        )


        return result.fetchone()[0]





# ==========================
# Save Job Skill Mapping
# ==========================

def save_job_skill(
    job_id,
    skill_id,
    confidence
):


    with engine.begin() as connection:


        connection.execute(

            text("""
                INSERT INTO job_skills
                (
                    job_id,
                    skill_id,
                    confidence_score
                )

                VALUES
                (
                    :job_id,
                    :skill_id,
                    :confidence
                )

                ON CONFLICT DO NOTHING

            """),

            {

                "job_id": job_id,

                "skill_id": skill_id,

                "confidence": confidence

            }

        )





# ==========================
# Batch Skill Extraction
# ==========================

def extract_skills_batch(
    jobs
):


    job_text = ""


    for job in jobs:

        description = (
            job.description
            or ""
        )


        job_text += f"""

JOB_ID:
{job.job_id}

DESCRIPTION:
{description[:MAX_DESCRIPTION_LENGTH]}

---------------------

"""



    prompt = f"""

You are extracting professional skills from multiple UK job descriptions.

For each job:

Return only skills explicitly required or clearly mentioned.

Rules:

- Extract 2-5 skills per job.
- Use standard professional skill names.
- Avoid generic phrases.
- Do not infer from job title only.
- Categorise each skill:

Technical
Business
Methodology
Domain
Soft Skill

Confidence:

1.0 explicit
0.7 strongly implied
0.5 weak


Return JSON only.

Format:

{{
 "jobs":[

  {{
   "job_id":"123",
   "skills":[

    {{
     "name":"Skill",
     "category":"Category",
     "confidence":0.9
    }}

   ]
  }}

 ]
}}

Jobs:

{job_text}

"""


    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role":"system",
                "content":prompt
            }

        ],

        temperature=TEMPERATURE,

        response_format={
            "type":"json_object"
        }

    )


    return json.loads(
        response
        .choices[0]
        .message
        .content
    )

# ==========================
# Process Batch Results
# ==========================

def save_batch_results(
    extraction_result
):


    saved = 0



    for job in extraction_result.get(
        "jobs",
        []
    ):


        job_id = job.get(
            "job_id"
        )


        for skill in job.get(
            "skills",
            []
        ):


            skill_id = get_or_create_skill(

                skill["name"],

                skill["category"]

            )


            save_job_skill(

                job_id,

                skill_id,

                skill.get(
                    "confidence",
                    0.5
                )

            )


        saved += 1



    return saved

# ==========================
# Load Jobs Without Skills
# ==========================

def load_unprocessed_jobs( limit=30 ):


    with engine.connect() as connection:


        result = connection.execute(

            text("""
                SELECT

                    job_id,

                    description


                FROM jobs


                WHERE description IS NOT NULL


                AND LENGTH(description) > 200


                AND NOT EXISTS

                (

                    SELECT 1

                    FROM job_skills js

                    WHERE js.job_id = jobs.job_id

                )


                LIMIT :limit

            """),

            {
                "limit": limit
            }

        )


        return result.fetchall()


# ==========================
# Retry Wrapper
# ==========================

def run_with_retry(

    jobs,

    retries=MAX_RETRIES

):


    for attempt in range(

        retries

    ):


        try:


            print(

                f"Groq attempt "
                f"{attempt + 1}/{retries}",

                flush=True

            )


            return (

                extract_skills_batch(

                    jobs

                )

            )


        except Exception as e:


            error_text = str(e)


            print()

            print(

                f"AI error on attempt "
                f"{attempt + 1}/{retries}",

                flush=True

            )


            print(

                error_text,

                flush=True

            )


            if (

                "TPD" in error_text

                or

                "tokens per day"

                in error_text

            ):


                print(

                    "Groq daily token "
                    "limit reached.",

                    flush=True

                )


                send_message(

                    """

🚫 Groq daily token limit reached

The pipeline stopped safely.

Run the pipeline again
after the limit resets.

"""

                )


                raise SystemExit(1)


            if (

                "429" in error_text

                and

                attempt

                <

                retries - 1

            ):


                wait = (

                    RETRY_DELAYS[

                        attempt

                    ]

                )


                print(

                    f"Waiting {wait} seconds "
                    f"before retry...",

                    flush=True

                )


                time.sleep(

                    wait

                )


                continue


            raise


    raise Exception(

        "Groq request failed "

        "after all retries."

    )



# ==========================
# Create Skill Demand Snapshot
# ==========================

def create_skill_demand_snapshot():


    today = datetime.now().date()



    with engine.begin() as connection:


        connection.execute(

            text("""
                INSERT INTO skill_demand_snapshots

                (
                    snapshot_date,

                    skill_id,

                    job_count

                )


                SELECT

                    :snapshot_date,

                    skill_id,

                    COUNT(job_id)


                FROM job_skills


                GROUP BY skill_id


                ON CONFLICT

                (
                    snapshot_date,

                    skill_id

                )


                DO UPDATE SET

                    job_count = EXCLUDED.job_count

            """),

            {

                "snapshot_date": today

            }

        )



    print(
        "Skill demand snapshot created"
    )





# ==========================
# Print Top Skills
# ==========================

def print_top_skills(
    limit=20
):


    with engine.connect() as connection:


        result = connection.execute(

            text("""
                SELECT

                    s.skill_name,

                    s.category,

                    SUM(
                        sds.job_count
                    )
                    AS demand


                FROM skill_demand_snapshots sds


                JOIN skills s

                ON s.skill_id =
                   sds.skill_id


                GROUP BY

                    s.skill_name,

                    s.category


                ORDER BY

                    demand DESC


                LIMIT :limit

            """),

            {

                "limit": limit

            }

        )


        rows = result.fetchall()



    print()

    print(
        "=============================="
    )

    print(
        "TOP SKILLS"
    )

    print(
        "=============================="
    )



    for row in rows:


        print(

            f"{row.skill_name} | "
            f"{row.category} | "
            f"Demand: {row.demand}"

        )





# ==========================
# Pipeline Report
# ==========================

def print_pipeline_report():


    with engine.connect() as connection:


        jobs = connection.execute(

            text("""
                SELECT COUNT(*)

                FROM jobs

            """)

        ).scalar()



        skills = connection.execute(

            text("""
                SELECT COUNT(*)

                FROM skills

            """)

        ).scalar()



        mappings = connection.execute(

            text("""
                SELECT COUNT(*)

                FROM job_skills

            """)

        ).scalar()



    report = {


        "jobs": jobs,


        "skills": skills,


        "job_skill_mappings": mappings,


        "generated_at":
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    }



    print()

    print(
        "=============================="
    )

    print(
        "PIPELINE REPORT"
    )

    print(
        json.dumps(
            report,
            indent=4
        )

    )

# ==========================
# Main Pipeline
# ==========================

def main():


    start_time = datetime.now()


    print()

    print(
        "=============================="
    )

    print(
        "START AI BATCH SKILL PIPELINE"
    )

    send_message(

        """

        🚀 AI Skill Extraction Started

        The batch skill extraction
        pipeline is now running.

    """
    )

    print(
        "=============================="
    )



    # Number of jobs to process

    JOB_LIMIT = 500



    jobs = load_unprocessed_jobs( JOB_LIMIT )


    total_jobs = len(jobs)



    print()

    print(
        f"Jobs waiting for extraction: {total_jobs}"
    )



    if total_jobs == 0:


        print(
            "No new jobs found"
        )


    else:


        batches = list(

            chunk_list(

                jobs,

                BATCH_SIZE

            )

        )



        total_batches = len(
            batches
        )


        processed_jobs = 0


        errors = 0



        for index, batch in enumerate(
            batches,
            start=1
        ):


            print()

            print(
                "=============================="
            )

            print(
                f"Batch {index}/{total_batches}"
            )

            print(
                f"Jobs in batch: {len(batch)}"
            )



            try:


                batch_start = (

                    datetime.now()

                )


                result = (

                    run_with_retry(

                        batch

                    )

                )


                print(

                    "Saving batch results "
                    "to Neon...",

                    flush=True

                )


                saved = (

                    save_batch_results(

                        result

                    )

                )


                batch_duration = (

                    datetime.now()

                    -

                    batch_start

                )


                processed_jobs += saved


                print(

                    f"Saved jobs: {saved}",

                    flush=True

                )


                print(

                    f"Batch duration: "
                    f"{batch_duration}",

                    flush=True

                )
            
            except Exception as e:


                errors += len(batch)
                
                send_message(
                f"""
                    ❌ AI Skill Extraction Failed

                    {str(e)}
                    """
                )

                print(
                    "Batch failed:"
                )

                print(e)



            # small delay between requests

            time.sleep(
                3
            )



        print()

        print(
            "=============================="
        )

        print(
            "PROCESS RESULTS"
        )

        print(
            "=============================="
        )


        print(
            "Total jobs:",
            total_jobs
        )


        print(
            "Processed:",
            processed_jobs
        )


        print(
            "Errors:",
            errors
        )




    # Update analytics tables

    create_skill_demand_snapshot()
    print_top_skills()
    print_pipeline_report()

    duration = (
        datetime.now()
        -
        start_time
    )

    print()

    print(
        "=============================="
    )

    print(
        "AI BATCH PIPELINE FINISHED"
    )
    
    send_message(
        f"""
        ✅ AI Skill Extraction Finished
        """
    )

    print(
        "=============================="
    )


    print(
        "Duration:",
        duration
    )





# ==========================
# Entry Point
# ==========================

if __name__ == "__main__":


    main()