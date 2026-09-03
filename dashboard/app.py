# dashboard/app.py
"""
Streamlit dashboard for Madrid Airbnb data analysis.
Entry point of the application.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
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

# --- Apply filters to the dataframe ---
# This filtered dataframe will be reused across all tabs
df_filtered = df[
    (df["neighbourhood_group"].isin(selected_districts))
    & (df["room_type"].isin(selected_room_types))
    & (df["price"] >= selected_price_range[0])
    & (df["price"] <= selected_price_range[1])
]

# --- Main title ---
st.title("🏠 Madrid Airbnb Dashboard")
st.caption("Análisis enriquecido con datos de renta, población, alquiler y VUT por distrito")

# --- Tabs ---
tab_summary, tab_price, tab_income = st.tabs(
    ["Resumen general", "Precios por distrito", "Precio vs Renta/Población"]
)

with tab_summary:
    st.subheader("Indicadores generales")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Nº de alojamientos", f"{len(df_filtered):,}")
    col2.metric("Precio medio", f"{df_filtered['price'].mean():.0f} €")
    col3.metric("Precio mediana", f"{df_filtered['price'].median():.0f} €")
    col4.metric("Distritos representados", df_filtered["neighbourhood_group"].nunique())

    st.divider()
    st.write("Vista previa de los datos filtrados:")
    st.dataframe(df_filtered.head(10))

with tab_price:
    st.subheader("Distribución de precios por distrito")

    # Order districts by median price (descending) for a clearer reading
    order = (
        df_filtered.groupby("neighbourhood_group")["price"]
        .median()
        .sort_values(ascending=False)
        .index
    )

    fig_box = px.box(
        df_filtered,
        x="neighbourhood_group",
        y="price",
        category_orders={"neighbourhood_group": list(order)},
        labels={"neighbourhood_group": "Distrito", "price": "Precio (€)"},
    )
    fig_box.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig_box, use_container_width=True)

with tab_income:
    st.write("Relación precio vs renta/población — próximo paso")