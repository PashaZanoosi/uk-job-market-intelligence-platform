import os
import json
import time
import requests

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


APP_ID = os.getenv(
    "ADZUNA_APP_ID"
)

APP_KEY = os.getenv(
    "ADZUNA_APP_KEY"
)


BASE_URL = (
    "https://api.adzuna.com/v1/api/jobs/gb/search/"
)

RESULTS_PER_PAGE = 50
MAX_REQUESTS_PER_RUN = 83
RETRY_LIMIT = 3

RETRY_DELAYS = [
    10,
    30,
    60
]



# ==========================
# Fetch one page
# ==========================

def fetch_page(page):


    url = (
        BASE_URL
        +
        str(page)
    )


    params = {

        "app_id": APP_ID,

        "app_key": APP_KEY,

        "results_per_page":
            RESULTS_PER_PAGE,

        "sort_by":
            "date"

    }



    for attempt in range(RETRY_LIMIT):


        try:

            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            print(
                "ADZUNA RESPONSE:",
                response.status_code
            )


            if response.status_code == 200:

                return response.json()



            print(
                f"Page {page}: API Error {response.status_code}"
            )



        except Exception as e:


            print(
                f"Page {page}: Request failed"
            )

            print(e)



        if attempt < RETRY_LIMIT - 1:


            wait = RETRY_DELAYS[attempt]


            print(
                f"Retrying page {page} in {wait} seconds..."
            )


            time.sleep(
                wait
            )



    raise Exception(

        f"Adzuna API failed after {RETRY_LIMIT} attempts on page {page}"

    )




# ==========================
# Collect Jobs
# ==========================

def collect_jobs():


    all_jobs = []

    requests_count = 0

    api_total = 0



    print("==============================")
    print("START ADZUNA COLLECTION")
    print("==============================")



    for page in range(
        1,
        MAX_REQUESTS_PER_RUN + 1
    ):


        print(
            f"Requesting page {page}/{MAX_REQUESTS_PER_RUN}"
        )


        data = fetch_page(
            page
        )


        requests_count += 1


        api_total = data.get(
            "count",
            0
        )


        results = data.get(
            "results",
            []
        )


        all_jobs.extend(
            results
        )

        print(
            f"Completed page {page}/{MAX_REQUESTS_PER_RUN} | "
            f"Jobs collected so far: {len(all_jobs)}",
            flush=True
        )

        time.sleep(
            2.5
        )

    return (

        all_jobs,

        requests_count,

        api_total

    )

# ==========================
# Statistics
# ==========================

def print_statistics(
    jobs,
    requests_count,
    api_total
):


    print()

    print("==============================")
    print("JOB DATA STATISTICS")
    print("==============================")


    print(
        "API requests:",
        requests_count
    )


    print(
        "Total job records:",
        len(jobs)
    )

    job_ids = set()
    titles = set()
    companies = set()

    for job in jobs:


        if job.get("id"):

            job_ids.add(
                job["id"]
            )



        if job.get("title"):

            titles.add(
                job["title"]
            )



        company = job.get(
            "company",
            {}
        )


        if isinstance(company, dict):

            name = company.get(
                "display_name"
            )


            if name:

                companies.add(
                    name
                )



    print(
        "Unique job IDs:",
        len(job_ids)
    )


    print(
        "Unique job titles:",
        len(titles)
    )


    print(
        "Unique companies:",
        len(companies)
    )


    print(
        "Adzuna reported total results:",
        api_total
    )


    print("==============================")

# ==========================
# Main
# ==========================

if __name__ == "__main__":

    jobs, requests_count, api_total = collect_jobs()

    data = {

        "collected_at":
            datetime.now().isoformat(),

        "count":
            api_total,

        "results":
            jobs

    }



    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    filename = (

        "data/raw/jobs_"
        +
        datetime.now().strftime(
            "%Y%m%d"
        )
        +
        ".json"
    )

    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as file:


        json.dump(

            data,

            file,

            ensure_ascii=False,

            indent=4

        )

    print_statistics(

        jobs,

        requests_count,

        api_total

    )

    print(
        f"Saved: {filename}"
    )

    print(
        "Finished"
    )