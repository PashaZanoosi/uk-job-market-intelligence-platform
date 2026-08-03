# =====================================================
# load_master_parquet.py
# Load Adzuna Master Parquet Into Neon
# =====================================================

import pandas as pd

from sqlalchemy import text

from src.database.connection import engine
from src.utils.google_drive import download_parquet_dataframe


# =====================================================
# Configuration
# =====================================================

PARQUET_FILE = "uk_jobs_master.parquet"

BATCH_SIZE = 100

# =====================================================
# Helpers
# =====================================================

def clean_value(value):

    if pd.isna(value):
        return None

    return value



def calculate_average_salary(
    salary_min,
    salary_max
):

    if (
        salary_min is not None
        and salary_max is not None
    ):

        return int(
            (
                float(salary_min)
                +
                float(salary_max)
            )
            /
            2
        )

    return None



# =====================================================
# Prepare Data
# =====================================================

def prepare_records(df):

    records = []


    for _, row in df.iterrows():


        salary_min = clean_value(
            row.get("salary_min")
        )


        salary_max = clean_value(
            row.get("salary_max")
        )


        record = {

            "job_id":
                str(
                    row["job_id"]
                ),


            "title":
                clean_value(
                    row.get("title")
                ),


            "description":
                clean_value(
                    row.get("description")
                ),


            "company_name":
                clean_value(
                    row.get("company_name")
                ),


            # old column
            "category":
                clean_value(
                    row.get("category_label")
                ),


            # old column
            "location":
                clean_value(
                    row.get("location_display_name")
                ),


            "salary_min":
                salary_min,


            "salary_max":
                salary_max,


            "average_salary":
                calculate_average_salary(
                    salary_min,
                    salary_max
                ),


            "first_seen_date":
                clean_value(
                    row.get("first_seen_date")
                ),


            "redirect_url":
                clean_value(
                    row.get("redirect_url")
                ),


            "category_label":
                clean_value(
                    row.get("category_label")
                ),


            "location_area":
                clean_value(
                    row.get("location_area")
                ),


            "last_seen_date":
                clean_value(
                    row.get("last_seen_date")
                )

        }


        records.append(
            record
        )


    return records



# =====================================================
# Insert
# =====================================================

def insert_records(records):


    sql = text("""

        INSERT INTO jobs
        (

            job_id,

            title,

            description,

            company_name,

            category,

            location,

            salary_min,

            salary_max,

            average_salary,

            first_seen_date,

            redirect_url,

            category_label,

            location_area,

            last_seen_date

        )


        VALUES

        (

            :job_id,

            :title,

            :description,

            :company_name,

            :category,

            :location,

            :salary_min,

            :salary_max,

            :average_salary,

            :first_seen_date,

            :redirect_url,

            :category_label,

            :location_area,

            :last_seen_date

        )


        ON CONFLICT (job_id)

        DO NOTHING


    """)


    inserted = 0
    skipped = 0
    errors = 0


    with engine.connect() as connection:


        for index, record in enumerate(
            records,
            start=1
        ):


            try:

                result = connection.execute(
                    sql,
                    record
                )


                if result.rowcount == 1:

                    inserted += 1

                else:

                    skipped += 1



                if index % BATCH_SIZE == 0:

                    connection.commit()

                    print(
                        f"Inserted {index}/{len(records)}",
                        flush=True
                    )



            except Exception as e:


                errors += 1

                connection.rollback()


                print(
                    "ERROR JOB:",
                    record["job_id"]
                )

                print(
                    e
                )



        connection.commit()



    return (
        inserted,
        skipped,
        errors
    )



# =====================================================
# Main
# =====================================================

def main():


    print("==============================")
    print("START MASTER PARQUET LOAD")
    print("==============================")


    print(
        "Reading parquet from Google Drive..."
    )


    df = download_parquet_dataframe(
        PARQUET_FILE
    )


    print(
        "Parquet rows:",
        len(df)
    )



    print(
        "Preparing records..."
    )


    records = prepare_records(
        df
    )


    print(
        "Prepared:",
        len(records)
    )



    inserted, skipped, errors = insert_records(
        records
    )



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


    print("==============================")
    print("MASTER PARQUET LOAD FINISHED")
    print("==============================")



if __name__ == "__main__":

    main()