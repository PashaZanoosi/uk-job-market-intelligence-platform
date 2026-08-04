# =====================================================
# skill_pipeline.py
# Main Skill Extraction Pipeline
# =====================================================


from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)


from sqlalchemy import text


from src.database.connection import engine


from src.skills.job_selector import get_pending_jobs


from src.skills.description_scraper import scrape_description


from src.skills.skill_extractor import extract_skills


from src.skills.skill_database import save_job_skills



# =====================================================
# Update Job Status
# =====================================================


def update_job_status(
    job_id,
    status,
    error=None
):


    sql = text("""
        UPDATE jobs

        SET

            skills_extraction_status = :status,

            skills_extraction_error = :error,

            skills_last_extracted_at = CURRENT_TIMESTAMP

        WHERE job_id = :job_id
    """)


    with engine.begin() as connection:


        connection.execute(

            sql,

            {

                "job_id": job_id,

                "status": status,

                "error": error

            }

        )




# =====================================================
# Process Single Job
# =====================================================


def process_job(job):


    print()
    print("-" * 60)

    print(
        f"JOB ID: {job.job_id}"
    )

    print(
        f"TITLE: {job.title}"
    )



    update_job_status(

        job.job_id,

        "processing"

    )



    # ---------------------------------
    # Scrape Description
    # ---------------------------------


    scrape_result = scrape_description(

        job.redirect_url,

        job.title

    )



    if scrape_result["status"] != "success":


        update_job_status(

            job.job_id,

            "unavailable",

            scrape_result["error_type"]

        )


        print(

            "Unavailable:",

            scrape_result["error_type"]

        )


        return False



    description = scrape_result["description"]



    print(

        "Description length:",

        len(description)

    )




    # ---------------------------------
    # Extract Skills
    # ---------------------------------


    extraction_result = extract_skills(

        [

            {

                "job_id": str(job.job_id),

                "description": description

            }

        ]

    )



    skills = extraction_result.get(

        "jobs",

        []

    )



    if skills:


        extracted_skills = skills[0].get(

            "skills",

            []

        )


    else:


        extracted_skills = []




    print()

    print(
        "Extracted skills:"
    )



    for skill in extracted_skills:


        print(

            f"- {skill['skill_name']} | "
            f"{skill['skill_type']} | "
            f"{skill['skill_category']}"

        )




    saved_count = save_job_skills(

        job.job_id,

        extracted_skills

    )



    print(

        f"Skills saved: {saved_count}"

    )




    update_job_status(

        job.job_id,

        "completed"

    )



    return True





# =====================================================
# Run Pipeline
# =====================================================


def run_skill_pipeline(

    batch_size=50,

    max_workers=5

):


    print("=" * 60)

    print(
        "START SKILL EXTRACTION PIPELINE"
    )

    print("=" * 60)




    jobs = get_pending_jobs(

        limit=batch_size

    )



    print(

        f"Jobs selected: {len(jobs)}"

    )




    success = 0

    failed = 0



    with ThreadPoolExecutor(

        max_workers=max_workers

    ) as executor:



        futures = [

            executor.submit(

                process_job,

                job

            )

            for job in jobs

        ]



        for future in as_completed(futures):


            try:


                result = future.result()



                if result:


                    success += 1


                else:


                    failed += 1



            except Exception as e:


                print(

                    "Worker error:",

                    e

                )


                failed += 1





    print()

    print("=" * 60)

    print(
        "PIPELINE RESULT"
    )

    print("=" * 60)



    print(

        "Success:",

        success

    )



    print(

        "Failed:",

        failed

    )



    print("=" * 60)

    print(
        "SKILL PIPELINE FINISHED"
    )

    return {
    "success": success,
    "failed": failed,
    "processed": len(jobs)
    }






# =====================================================
# Entry Point
# =====================================================


if __name__ == "__main__":

    import os

    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))

    run_skill_pipeline(
        batch_size=BATCH_SIZE
    )