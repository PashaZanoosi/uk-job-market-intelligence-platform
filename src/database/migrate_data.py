from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os


load_dotenv()


LOCAL_DATABASE_URL = os.getenv(
    "LOCAL_DATABASE_URL"
)

NEON_DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


local_engine = create_engine(
    LOCAL_DATABASE_URL
)

neon_engine = create_engine(
    NEON_DATABASE_URL
)



tables = [

    "skill_taxonomy",

    "skills",

    "jobs",

    "job_skills",

    "job_snapshots",

    "skill_demand_snapshots",

    "taxonomy_demand_snapshots",

    "skill_taxonomy_suggestions"

]



print("==============================")
print("START DATABASE MIGRATION")
print("==============================")


for table in tables:


    print()

    print(
        "Migrating:",
        table
    )


    try:

        df = pd.read_sql(
            f"SELECT * FROM {table}",
            local_engine
        )


        print(
            "Rows found:",
            len(df)
        )


        if len(df) == 0:

            print(
                "Skipped: empty table"
            )

            continue



        df.to_sql(

            table,

            neon_engine,

            if_exists="append",

            index=False

        )


        print(
            "Inserted:",
            len(df)
        )



    except Exception as e:


        print(
            "ERROR:",
            e
        )



print()

print("==============================")
print("MIGRATION FINISHED")
print("==============================")