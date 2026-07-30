import streamlit as st


def page_header(title, description):

    st.title(title)

    st.caption(description)



def format_salary(value):

    if value is None:
        return "-"

    return f"£{value:,.2f}"



def metric_card(label, value):

    st.metric(
        label,
        value
    )