import streamlit as st

st.set_page_config(
    page_title="UK Job Market Intelligence", layout="wide" )

import streamlit as st


pages = {
    "Market Intelligence": [
        st.Page(
            "pages/1_Overview.py",
            title="1 - Overview"
        ),
        st.Page(
            "pages/2_Skills.py",
            title="2 - Skills Intelligence"
        ),
        st.Page(
            "pages/3_Market.py",
            title="3 - Market Analysis"
        ),
        st.Page(
            "pages/4_Trends.py",
            title="4 - Historical Trends"
        ),
        st.Page(
            "pages/5_Pipeline.py",
            title="5 - AI Pipeline"
        )
    ]
}


pg = st.navigation(pages)

pg.run()