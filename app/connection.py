import streamlit as st
from sqlalchemy import create_engine


def get_connection():

    db_config = st.secrets["postgres"]

    connection_string = (
        f"postgresql+psycopg2://"
        f"{db_config['user']}:"
        f"{db_config['password']}@"
        f"{db_config['host']}:"
        f"{db_config['port']}/"
        f"{db_config['database']}"
    )

    engine = create_engine(connection_string)

    return engine