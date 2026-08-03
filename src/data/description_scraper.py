import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))


import requests
import pandas as pd

from bs4 import BeautifulSoup

from sqlalchemy import text
from src.database.connection import engine



HEADERS = {

    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/138.0.0.0 Safari/537.36"

}



# =====================================
# Load jobs
# =====================================

with engine.connect() as connection:

    result = connection.execute(

        text("""
            SELECT
                job_id,
                title,
                redirect_url

            FROM jobs

            WHERE redirect_url IS NOT NULL

            LIMIT 10
        """)

    )

    jobs = result.fetchall()



print(f"Loaded jobs: {len(jobs)}")



# =====================================
# HTML to text
# =====================================

def extract_page_text(html):

    soup = BeautifulSoup(

        html,

        "html.parser"

    )


    return soup.get_text(

        " ",

        strip=True

    )



# =====================================
# Detect Adzuna protection
# =====================================

def detect_block(response):


    if response.status_code in [

        403,

        429,

        503

    ]:

        return True, f"http_{response.status_code}"



    html = response.text.lower()


    block_words = [

        "captcha",

        "cloudflare",

        "verify you are human",

        "access denied",

        "checking your browser",

        "unusual traffic"

    ]


    for word in block_words:

        if word in html:

            return True, word



    return False, None



# =====================================
# Find job content start
# =====================================

def extract_job_start(page_text, title):


    if not title:

        return page_text



    title_index = page_text.find(title)



    if title_index == -1:

        return page_text



    text_after_title = page_text[

        title_index + len(title):

    ]



    start_points = [


        "About the job",

        "About The Job",


        "The Role",


        "We are looking",

        "We're looking",

        "We’re looking",


        "We are currently looking",


        "At ",

        "As a ",

        "You will "

    ]



    positions = []



    for point in start_points:


        index = text_after_title.find(point)


        if index != -1:

            positions.append(index)



    if positions:


        start = min(positions)


        return text_after_title[start:]



    # fallback

    words = text_after_title.split()



    return " ".join(words[40:])



# =====================================
# Remove footer
# =====================================

def clean_footer(text):


    endings = [


        "Apply for this job",

        "Stats for this job",

        "Salary comparison",

        "Similar jobs",

        "Popular searches",

        "Receive similar jobs by email",

        "Create alert"

    ]



    for ending in endings:


        index = text.find(ending)


        if index != -1:

            text = text[:index]



    return text.strip()



# =====================================
# Main scraper test
# =====================================

results = []



for i, job in enumerate(jobs, start=1):


    print(

        f"{i}/{len(jobs)} {job.job_id}"

    )


    try:


        response = requests.get(

            job.redirect_url,

            headers=HEADERS,

            timeout=20,

            allow_redirects=True

        )



        # ------------------------------
        # 404
        # ------------------------------

        if response.status_code == 404:


            results.append(

                {

                    "job_id":

                        job.job_id,

                    "title":

                        job.title,

                    "status_code":

                        404,

                    "error_type":

                        "page_not_found",

                    "html_length":

                        len(response.text),

                    "description_length":

                        0,

                    "description":

                        ""

                }

            )


            continue



        # ------------------------------
        # Block detection
        # ------------------------------

        blocked, reason = detect_block(response)



        if blocked:


            results.append(

                {

                    "job_id":

                        job.job_id,

                    "title":

                        job.title,

                    "status_code":

                        response.status_code,

                    "error_type":

                        reason,

                    "html_length":

                        len(response.text),

                    "description_length":

                        0,

                    "description":

                        ""

                }

            )


            continue



        # ------------------------------
        # Extract
        # ------------------------------

        page_text = extract_page_text(

            response.text

        )



        description = extract_job_start(

            page_text,

            job.title

        )



        description = clean_footer(

            description

        )



        results.append(

            {

                "job_id":

                    job.job_id,


                "title":

                    job.title,


                "status_code":

                    response.status_code,


                "error_type":

                    None,


                "html_length":

                    len(response.text),


                "description_length":

                    len(description),


                "description":

                    description[:6000]

            }

        )



        print(

            "Description length:",

            len(description)

        )



    except Exception as e:


        print(

            "ERROR:",

            e

        )


        results.append(

            {

                "job_id":

                    job.job_id,


                "title":

                    job.title,


                "status_code":

                    None,


                "error_type":

                    str(e),


                "html_length":

                    0,


                "description_length":

                    0,


                "description":

                    ""

            }

        )



# =====================================
# Save result
# =====================================

df = pd.DataFrame(results)



df.to_csv(

    "clean_description_test.csv",

    index=False,

    encoding="utf-8-sig"

)



print()

print("==========================")

print("FINISHED")

print("==========================")



print(

    df[

        [

            "status_code",

            "error_type",

            "description_length"

        ]

    ]

)