import time
from datetime import datetime

from sqlalchemy import text

from src.database.connection import engine


class PipelineLogger:

    def __init__(self, pipeline_name):

        self.pipeline_name = pipeline_name
        self.run_id = None
        self.start_time = None
        self.start_timestamp = None


    def start(self, source_rows=None):

        self.start_time = time.time()
        self.start_timestamp = datetime.utcnow()


        sql = text("""
            INSERT INTO pipeline_runs
            (
                pipeline_name,
                started_at,
                status,
                source_rows
            )

            VALUES
            (
                :pipeline_name,
                :started_at,
                :status,
                :source_rows
            )

            RETURNING run_id
        """)


        with engine.connect() as connection:

            result = connection.execute(
                sql,
                {
                    "pipeline_name":
                        self.pipeline_name,

                    "started_at":
                        self.start_timestamp,

                    "status":
                        "RUNNING",

                    "source_rows":
                        source_rows
                }
            )


            self.run_id = result.scalar()

            connection.commit()


        return self.run_id



    def finish(
        self,
        status="SUCCESS",
        inserted_rows=0,
        skipped_rows=0,
        error_count=0,
        error_message=None
    ):


        finish_timestamp = datetime.utcnow()


        duration = None

        if self.start_time:

            duration = int(
                time.time()
                -
                self.start_time
            )


        sql = text("""
            UPDATE pipeline_runs

            SET

                finished_at = :finished_at,

                status = :status,

                inserted_rows = :inserted_rows,

                skipped_rows = :skipped_rows,

                error_count = :error_count,

                error_message = :error_message,

                duration_seconds = :duration_seconds


            WHERE run_id = :run_id
        """)



        with engine.connect() as connection:

            connection.execute(
                sql,
                {

                    "finished_at":
                        finish_timestamp,

                    "status":
                        status,

                    "inserted_rows":
                        inserted_rows,

                    "skipped_rows":
                        skipped_rows,

                    "error_count":
                        error_count,

                    "error_message":
                        error_message,

                    "duration_seconds":
                        duration,

                    "run_id":
                        self.run_id

                }
            )


            connection.commit()