from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any


# ==========================
# Pipeline Result Object
# ==========================

@dataclass
class PipelineResult:
    step: str
    status: str
    processed: int = 0
    created: int = 0
    updated: int = 0
    errors: int = 0
    duration_seconds: float = 0
    message: str = ""
    timestamp: str = ""

    def __post_init__(self):

        if not self.timestamp:

            self.timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    # Convert object to dictionary

    def to_dict(self) -> Dict[str, Any]:

        return asdict(self)



    # Short summary for logs / Telegram

    def summary(self) -> str:

        return f"""
Step:
{self.step}

Status:
{self.status}

Processed:
{self.processed}

Created:
{self.created}

Updated:
{self.updated}

Errors:
{self.errors}

Duration:
{self.duration_seconds}s

Message:
{self.message}

Time:
{self.timestamp}
"""



# ==========================
# Factory Functions
# ==========================


def success_result(

    step: str,

    processed: int = 0,

    created: int = 0,

    updated: int = 0,

    errors: int = 0,

    duration_seconds: float = 0,

    message: str = ""

) -> PipelineResult:


    return PipelineResult(

        step=step,

        status="success",

        processed=processed,

        created=created,

        updated=updated,

        errors=errors,

        duration_seconds=duration_seconds,

        message=message

    )



def failed_result(

    step: str,

    error: Exception,

    processed: int = 0,

    created: int = 0,

    updated: int = 0,

    duration_seconds: float = 0

) -> PipelineResult:


    return PipelineResult(

        step=step,

        status="failed",

        processed=processed,

        created=created,

        updated=updated,

        errors=1,

        duration_seconds=duration_seconds,

        message=str(error)

    )



# ==========================
# Pipeline Aggregator
# ==========================


class PipelineReport:


    def __init__(self):

        self.results = []



    def add(

        self,

        result: PipelineResult

    ):

        self.results.append(
            result
        )



    def total_processed(self):

        return sum(
            r.processed
            for r in self.results
        )



    def total_created(self):

        return sum(
            r.created
            for r in self.results
        )



    def total_errors(self):

        return sum(
            r.errors
            for r in self.results
        )



    def is_successful(self):

        return all(

            r.status == "success"

            for r in self.results

        )



    def to_dict(self):

        return {

            "status":

                "success"
                if self.is_successful()
                else "failed",


            "steps":

                [

                    r.to_dict()

                    for r in self.results

                ],


            "summary":

                {

                    "total_processed":
                        self.total_processed(),


                    "total_created":
                        self.total_created(),


                    "total_errors":
                        self.total_errors()

                }

        }



    def telegram_message(self):

        status = (
            "✅"
            if self.is_successful()
            else
            "❌"
        )


        message = f"""
{status} JOB MARKET PIPELINE REPORT


Steps:
{len(self.results)}


Processed:
{self.total_processed()}


Created:
{self.total_created()}


Errors:
{self.total_errors()}


"""


        for result in self.results:

            message += f"""

------------------

{result.step}

Status:
{result.status}

Processed:
{result.processed}

Created:
{result.created}

Errors:
{result.errors}

Duration:
{result.duration_seconds}s

"""


        return message