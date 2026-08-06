import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

from connection import get_connection
from queries import SKILL_COOCCURRENCE_QUERY


st.set_page_config(
    page_title="Network",
    page_icon="🕸️",
    layout="wide"
)


@st.cache_data
def load_data(query):
    engine = get_connection()
    return pd.read_sql(query, engine)


df = load_data(SKILL_COOCCURRENCE_QUERY)


st.title("🕸️ Skill Network")


# -----------------------------
# Clean Data
# -----------------------------

df = df[
    df["skill_1"].notna()
    & df["skill_2"].notna()
]


# -----------------------------
# Filter
# -----------------------------

min_connection = st.slider(
    "Minimum Skill Connection",
    min_value=1,
    max_value=int(
        df["cooccurrence_count"].max()
    ),
    value=2
)


network_df = df[
    df["cooccurrence_count"] >= min_connection
]


# -----------------------------
# Build Graph
# -----------------------------

G = nx.Graph()


for _, row in network_df.iterrows():

    G.add_edge(
        row["skill_1"],
        row["skill_2"],
        weight=row["cooccurrence_count"]
    )


pos = nx.spring_layout(
    G,
    seed=42,
    k=0.8
)


# -----------------------------
# Edges
# -----------------------------

edge_x = []
edge_y = []


for edge in G.edges():

    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]

    edge_x += [
        x0,
        x1,
        None
    ]

    edge_y += [
        y0,
        y1,
        None
    ]


edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    mode="lines",
    line=dict(
        width=0.5
    ),
    hoverinfo="none"
)


# -----------------------------
# Nodes
# -----------------------------

node_x = []
node_y = []
node_text = []


for node in G.nodes():

    x, y = pos[node]

    node_x.append(x)
    node_y.append(y)

    node_text.append(
        node
    )


node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    text=node_text,
    textposition="top center",
    hoverinfo="text",
    marker=dict(
        size=15
    )
)


# -----------------------------
# Figure
# -----------------------------

fig = go.Figure(
    data=[
        edge_trace,
        node_trace
    ],
    layout=go.Layout(
        height=800,
        showlegend=False,
        hovermode="closest",
        margin=dict(
            b=20,
            l=5,
            r=5,
            t=20
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        )
    )
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------
# Supporting Table
# -----------------------------

st.divider()

st.subheader(
    "Strongest Skill Relationships"
)


table = network_df.sort_values(
    "cooccurrence_count",
    ascending=False
).head(30)


table.columns = [
    "Skill 1",
    "Skill 1 Type",
    "Skill 1 Category",
    "Skill 2",
    "Skill 2 Type",
    "Skill 2 Category",
    "Connection Strength",
    "Average Salary"
]


st.dataframe(
    table,
    hide_index=True,
    use_container_width=True
)