"""
PER FUNCIONAR S'HA DE FER $> streamlit run web.py
i s'obrirà al port que digui, segurament a localhost:8501
"""

import json
import os

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")   # must be the first Streamlit call


def placeholder(height):
    """Empty white box with a thin border."""
    return (
        alt.Chart(pd.DataFrame({"x": [0]}))
        .mark_point(opacity=0)
        .properties(height=height)
        .configure_view(fill="white", stroke="black")
    )


def load_spec(name):
    """Load an exported Vega-Lite spec as a plain dict (works for concat charts)."""
    path = os.path.join("outputs", f"{name}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# Top row: two charts, left narrower than right
col_left, col_right = st.columns([3, 4])
with col_left:
    st.altair_chart(placeholder(350), width="stretch")
with col_right:
    st.altair_chart(placeholder(350), width="stretch")

# Bottom: two full-width charts, one per row
q3 = load_spec("Q3")
if q3 is not None:
    st.vega_lite_chart(q3)            # small multiples keep the size set in the notebook
else:
    st.warning("outputs/Q3.json not found")
    st.altair_chart(placeholder(180), width="stretch")

st.altair_chart(placeholder(180), width="stretch")