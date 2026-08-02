import subprocess
import sys

from datetime import datetime

from src.utils.telegram_alert import send_message

from src.utils.logger import (
    logger,
    log_pipeline_start,
    log_pipeline_end
)


# ==========================
# Pipeline Steps
# ==========================

steps = [

    "src.data.get_jobs",

    "src.data.clean_jobs",

    "src.data.load_to_database",

    "src.ai.extract_skills",

    "src.ai.classify_skills",

    "src.ai.suggest_taxonomy",

    "src.analytics.create_snapshots",

    "src.analytics.market_insights"

]


# ==========================
# Start
# ==========================

print("==============================")
print("START JOB MARKET PIPELINE")
print("==============================", flush=True)


start_time = datetime.now()


log_pipeline_start()


send_message(
    "🚀 JOB Market Pipeline started"
)


# ==========================
# Run Pipeline
# ==========================

try:


    for step in steps:


        print()

        print("==============================")
        print(
            "RUNNING:",
            step
        )
        print("==============================", flush=True)


        logger.info(
            f"RUNNING: {step}"
        )


        process = subprocess.Popen(

            [

                sys.executable,

                "-m",

                step

            ],

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,

            text=True,

            bufsize=1

        )


        output_lines = []


        for line in process.stdout:

            print(
                line,
                end="",
                flush=True
            )

            output_lines.append(
                line
            )


        process.wait()


        output = "".join(
            output_lines
        )


        if output:

            logger.info(
                output
            )


        if process.returncode != 0:


            error_message = f"""

❌ Pipeline failed

Step:
{step}


Output:

{output}

"""


            logger.error(
                f"FAILED: {step}"
            )


            send_message(
                error_message
            )


            sys.exit(1)



        print()

        print(
            "COMPLETED:",
            step
        )

        print(
            flush=True
        )


        logger.info(
            f"COMPLETED: {step}"
        )



    # ==========================
    # Success
    # ==========================


    end_time = datetime.now()


    duration = (
        end_time - start_time
    )


    success_message = f"""

✅ JOB Market Pipeline completed


Started:

{start_time}


Finished:

{end_time}


Duration:

{duration}

"""


    logger.info(
        "Pipeline completed successfully"
    )


    logger.info(
        f"Duration: {duration}"
    )


    send_message(
        success_message
    )


    log_pipeline_end()


    print("==============================")
    print("PIPELINE FINISHED")
    print("==============================")

    print(
        "Duration:",
        duration
    )



except Exception as e:


    logger.exception(
        "Pipeline crashed"
    )


    error_message = f"""

❌ Pipeline crashed


Error:

{str(e)}

"""


    send_message(
        error_message
    )


    raise