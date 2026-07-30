import pandas as pd

from datetime import date


MASTER_FILE = "uk_jobs_master.parquet"


def update_master_jobs(
    new_jobs,
    existing_jobs=None
):

    today = date.today()


    # First run
    if existing_jobs is None or existing_jobs.empty:

        new_jobs["first_seen_date"] = today

        new_jobs["last_seen_date"] = today

        return new_jobs



    existing_jobs = existing_jobs.copy()



    new_jobs = new_jobs.copy()



    # Find existing IDs

    existing_ids = set(
        existing_jobs["job_id"]
    )



    new_jobs_ids = set(
        new_jobs["job_id"]
    )



    # New records

    new_records = new_jobs[
        ~new_jobs["job_id"].isin(existing_ids)
    ].copy()



    new_records["first_seen_date"] = today

    new_records["last_seen_date"] = today



    # Existing records found again

    existing_records = new_jobs[
        new_jobs["job_id"].isin(existing_ids)
    ][
        [
            "job_id"
        ]
    ]



    existing_jobs.loc[
        existing_jobs["job_id"].isin(
            existing_records["job_id"]
        ),
        "last_seen_date"
    ] = today



    # Merge

    updated = pd.concat(

        [
            existing_jobs,
            new_records
        ],

        ignore_index=True

    )



    # Safety duplicate removal

    updated = updated.drop_duplicates(
        subset=[
            "job_id"
        ],
        keep="last"
    )


    required_columns = {
        "skills_extracted": False,
        "skills_classified": False
    }

    for column, default_value in required_columns.items():

        if column not in updated.columns:

            updated[column] = default_value

        else:

            updated[column] = updated[column].fillna(
                default_value
            )

    return updated