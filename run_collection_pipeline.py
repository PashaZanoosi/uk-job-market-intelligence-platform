from datetime import datetime

from src.data.get_jobs import collect_jobs
from src.data.transform_jobs import transform_jobs
from src.data.save_master import save_master_jobs


print("==============================")
print("START DAILY JOB COLLECTION")
print("==============================")


start_time = datetime.now()


try:

    # ==========================
    # Collect from Adzuna
    # ==========================

    jobs, requests_count, api_total = collect_jobs()


    print()

    print("==============================")
    print("ADZUNA RESULT")
    print("==============================")


    print(
        "API Requests:",
        requests_count
    )


    print(
        "Collected Jobs:",
        len(jobs)
    )


    print(
        "API Total Results:",
        api_total
    )



    # ==========================
    # Transform
    # ==========================

    print()

    print(
        "Transforming jobs..."
    )


    jobs_df = transform_jobs(
        jobs
    )


    print(
        "Transformed rows:",
        len(jobs_df)
    )



    # ==========================
    # Save Master
    # ==========================

    updated_master = save_master_jobs(
        jobs_df
    )


    print()

    print("==============================")
    print("COLLECTION COMPLETED")
    print("==============================")


    print(
        "Master rows:",
        len(updated_master)
    )


    duration = (
        datetime.now()
        -
        start_time
    )


    print(
        "Duration:",
        duration
    )



except Exception as e:


    print()

    print("==============================")
    print("PIPELINE FAILED")
    print("==============================")


    print(e)


    raise