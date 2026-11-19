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

def get_chart_height(source, fallback=400):
    if isinstance(source, (alt.TopLevelMixin, alt.Chart)):
        if getattr(source, "height", None) is not None and isinstance(source.height, (int, float)):
            return int(source.height)
        source = source.to_dict()

    if isinstance(source, dict):
        if isinstance(source.get("height"), (int, float)):
            return int(source["height"])
        if isinstance(source.get("spec"), dict):
            h = get_chart_height(source["spec"], None)
            if h is not None:
                return h
        for key in ("vconcat", "hconcat", "layer"):
            if isinstance(source.get(key), list):
                heights = [get_chart_height(child, 0) for child in source[key]]
                if any(heights):
                    return int(sum(heights) if key == "vconcat" else max(heights))
    return fallback

def show_spec(source, fallback_height=400, padding=200, border=True):
    if isinstance(source, str):
        name = source
        source = load_spec(name)
        if source is None:
            st.warning(f"outputs/{name}.json not found")
            source = placeholder(fallback_height)

    chart_h = get_chart_height(source, fallback=fallback_height)

    with st.container(border=border):
        if isinstance(source, (alt.TopLevelMixin, alt.Chart)):
            st.altair_chart(source, width="stretch")
        elif isinstance(source, dict): #permet small multiples
            st.vega_lite_chart(source, width="stretch")
        else:
            st.error(f"Unsupported chart type: {type(source).__name__}")

#Grafiquem amb layout


st.set_page_config(layout="wide")   # must be the first Streamlit call


col_left, col_right = st.columns([3, 4])
with col_left:
    show_spec("Q1V1", 380)
with col_right:
    show_spec("Q4", 350)

show_spec("Q3", 400)
show_spec("Q2", 400)

