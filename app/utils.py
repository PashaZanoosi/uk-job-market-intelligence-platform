import pandas as pd
from connection import get_connection


def load_data(query):

    engine = get_connection()

    df = pd.read_sql(query, engine)

    return df