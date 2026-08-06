from geopy.geocoders import Nominatim
import time
import pandas as pd

from utils.geo_cache import (
    load_coordinates,
    save_coordinates
)


geolocator = Nominatim(
    user_agent="uk_job_market_intelligence_platform"
)


def get_coordinates(location):

    cache_df = load_coordinates()

    if not cache_df.empty:

        existing = cache_df[
            cache_df["location"] == location
        ]

        if not existing.empty:

            return {
                "latitude": existing.iloc[0]["latitude"],
                "longitude": existing.iloc[0]["longitude"]
            }


    try:

        result = geolocator.geocode(
            f"{location}, UK"
        )

        if result:

            new_row = {
                "location": location,
                "latitude": result.latitude,
                "longitude": result.longitude
            }

            cache_df = pd.concat(
                [
                    cache_df,
                    pd.DataFrame([new_row])
                ],
                ignore_index=True
            )

            save_coordinates(
                cache_df
            )

            time.sleep(1)

            return new_row


    except Exception:

        pass


    return {
        "latitude": None,
        "longitude": None
    }


def add_coordinates(df):

    coordinates = []

    for location in df["location"]:

        coordinates.append(
            get_coordinates(location)
        )


    df["latitude"] = [
        x["latitude"]
        for x in coordinates
    ]

    df["longitude"] = [
        x["longitude"]
        for x in coordinates
    ]


    return df