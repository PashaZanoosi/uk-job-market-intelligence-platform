import logging
import os
from datetime import datetime

# Create logs folder
os.makedirs(
    "logs",
    exist_ok=True
)

log_file = "logs/pipeline.log"

# Logger configuration
logger = logging.getLogger(
    "labour_market_pipeline"
)

logger.setLevel(
    logging.INFO
)

# Prevent duplicate handlers
if not logger.handlers:

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(
        formatter
    )

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )

def log_pipeline_start():

    logger.info(
        "=============================="
    )

    logger.info(
        "LABOUR MARKET PIPELINE STARTED"
    )

    logger.info(
        f"Start time: {datetime.now()}"
    )

def log_pipeline_end():

    logger.info(
        "LABOUR MARKET PIPELINE FINISHED"
    )

    logger.info(
        f"Finish time: {datetime.now()}"
    )

    logger.info(
        "=============================="
    )