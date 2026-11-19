"""
PER FUNCIONAR S'HA DE FER $> streamlit run web.py
i s'obrirà al port que digui, segurament a localhost:8501
"""

import json
import os

import altair as alt
import pandas as pd
import streamlit as st



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
        assert f is not None, f"fitxer llegit {name} no acaba de funcionar"
        return json.load(f)


def show_spec(source, height=300):
    """Render a chart from a file name, a Vega-Lite dict, or an Altair chart."""
    if isinstance(source, str): #carrega la imatge
        name = source
        source = load_spec(name)
        if source is None:
            st.warning(f"outputs/{name}.json not found")
            source = placeholder(height)

    if isinstance(source, (alt.TopLevelMixin, alt.Chart)): #Per les charts soles
        st.altair_chart(source, width="stretch")

    elif isinstance(source, dict):      #pels small multiples
        st.vega_lite_chart(source, width="stretch")
    else:
        st.error(f"Unsupported chart type: {type(source).__name__}")

#Grafiquem amb layout


st.set_page_config(layout="wide")   # must be the first Streamlit call


col_left, col_right = st.columns([3, 4])
with col_left:
    show_spec("Q1V1", 350)
with col_right:
    show_spec("Q4", 350)

show_spec("Q3", 1800)
show_spec("Q2", 1800)
