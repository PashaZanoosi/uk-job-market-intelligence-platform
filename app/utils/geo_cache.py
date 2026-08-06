import os
import pandas as pd


FILE_PATH = "app/data/location_cache.csv"


def save_coordinates(df):

    os.makedirs(
        "app/data",
        exist_ok=True
    )

    df.to_csv(
        FILE_PATH,
        index=False
    )


def load_coordinates():

    if os.path.exists(FILE_PATH):

        return pd.read_csv(
            FILE_PATH
        )

    return pd.DataFrame()