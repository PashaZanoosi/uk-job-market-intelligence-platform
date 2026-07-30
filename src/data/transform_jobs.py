import pandas as pd
from datetime import datetime


def transform_jobs(jobs):

    today = datetime.now().date()

    rows = []


    for job in jobs:

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


        rows.append(

            {

                "job_id": int(job.get("id")),

                "title": job.get(
                    "title"
                ),

                "description": job.get(
                    "description"
                ),


                "company_name":
                    company.get(
                        "display_name"
                    ),


                "category_tag":
                    category.get(
                        "tag"
                    ),


                "category_label":
                    category.get(
                        "label"
                    ),


                "location_display_name":
                    location.get(
                        "display_name"
                    ),


                "location_area":
                    ", ".join(
                        location.get(
                            "area",
                            []
                        )
                    ),


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


                "contract_time":
                    job.get(
                        "contract_time"
                    ),


                "contract_type":
                    job.get(
                        "contract_type"
                    ),


                "created_date":
                    pd.to_datetime(
                        job.get(
                            "created"
                        )
                    ).date()
                    if job.get("created")
                    else None,


                "adref":
                    job.get(
                        "adref"
                    ),


                "redirect_url":
                    job.get(
                        "redirect_url"
                    ),


                # New tracking columns

                "first_seen_date":
                    today,


                "last_seen_date":
                    today,


                "collection_date":
                    today,


                # AI status

                "skills_extracted":
                    False,


                "skills_classified":
                    False

            }

        )


    df = pd.DataFrame(rows)


    return df