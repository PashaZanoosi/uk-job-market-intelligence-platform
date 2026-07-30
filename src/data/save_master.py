import pandas as pd
from datetime import datetime

from src.utils.google_drive import (
    download_parquet,
    upload_parquet
)


MASTER_FILE = "uk_jobs_master.parquet"



def save_master_jobs(new_jobs):


    print("==============================")
    print("UPDATING MASTER JOB STORAGE")
    print("==============================")


    print(
        "Downloading existing master file..."
    )


    existing_jobs = download_parquet(
        MASTER_FILE
    )


    today = datetime.now().date()



    if existing_jobs is None:


        print(
            "No existing master found."
        )


        master = new_jobs.copy()



    else:


        print(
            f"Existing jobs: {len(existing_jobs)}"
        )


        existing_jobs["job_id"] = (
            existing_jobs["job_id"]
            .astype(int)
        )


        new_jobs["job_id"] = (
            new_jobs["job_id"]
            .astype(int)
        )


        master = pd.concat(

            [
                existing_jobs,
                new_jobs
            ],

            ignore_index=True

        )


        # Remove duplicates by job_id

        master = (
            master
            .sort_values(
                "collection_date"
            )
            .drop_duplicates(
                subset=[
                    "job_id"
                ],
                keep="last"
            )
        )


        # Update seen dates

        new_ids = set(
            new_jobs["job_id"]
        )


        master.loc[
            master["job_id"].isin(new_ids),
            "last_seen_date"
        ] = today


        master.loc[
            master["job_id"].isin(new_ids),
            "collection_date"
        ] = today



    master = master.reset_index(
        drop=True
    )


    print(
        f"Master jobs after update: {len(master)}"
    )


    print(
        "Uploading master file..."
    )

    # Fix date consistency

    date_columns = [
        "created_date",
        "first_seen_date",
        "last_seen_date",
        "collection_date"
    ]


    for column in date_columns:

        if column in master.columns:

            for column in date_columns:

                if column in master.columns:

                    master[column] = master[column].apply(
                        lambda x:
                            pd.to_datetime(
                                x,
                                errors="coerce",
                                utc=True
                            )
                            .tz_localize(None)
                            .date()
                            if pd.notna(x)
                            else None
                    )

    upload_parquet(
        master,
        MASTER_FILE
    )


    print(
        "Master storage updated successfully."
    )


    return master