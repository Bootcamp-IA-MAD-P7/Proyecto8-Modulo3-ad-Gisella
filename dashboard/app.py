# dashboard/app.py
"""
Streamlit dashboard for Madrid Airbnb data analysis.
Entry point of the application.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# --- Page configuration ---
st.set_page_config(
    page_title="Madrid Airbnb Dashboard",
    page_icon="🏠",
    layout="wide",
)

# --- Data loading ---
# Path is built relative to this file, so it works no matter
# where the streamlit command is run from.
DATA_PATH = Path(__file__).parent.parent / "data" / "processed" / "madrid_airbnb_enriched.csv"


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """Load the enriched Airbnb dataset and cache it in memory."""
    return pd.read_csv(path)


df = load_data(DATA_PATH)

# --- Sidebar filters ---
st.sidebar.header("Filtros")

districts = sorted(df["neighbourhood_group"].unique())
selected_districts = st.sidebar.multiselect(
    "Distrito",
    options=districts,
    default=districts,  # all selected by default
)

room_types = sorted(df["room_type"].unique())
selected_room_types = st.sidebar.multiselect(
    "Tipo de habitación",
    options=room_types,
    default=room_types,
)

min_price, max_price = int(df["price"].min()), int(df["price"].max())
selected_price_range = st.sidebar.slider(
    "Rango de precio (€)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, 500),  # default upper bound at 500, same as your EDA df_viz
)

# --- Main title ---
st.title("🏠 Madrid Airbnb Dashboard")
st.caption("Análisis enriquecido con datos de renta, población, alquiler y VUT por distrito")

# --- Tabs ---
tab_summary, tab_price, tab_income = st.tabs(
    ["Resumen general", "Precios por distrito", "Precio vs Renta/Población"]
)

with tab_summary:
    st.write("KPIs generales — próximo paso")

with tab_price:
    st.write("Análisis de precios por distrito — próximo paso")

with tab_income:
    st.write("Relación precio vs renta/población — próximo paso")