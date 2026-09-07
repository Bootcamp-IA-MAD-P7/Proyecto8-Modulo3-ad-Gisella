# dashboard/app.py
"""
Streamlit dashboard for Madrid Airbnb data analysis.
Entry point of the application.
"""

from pathlib import Path

from scipy.stats import pearsonr
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
    st.subheader("Relación entre precio y variables socioeconómicas")

    variable = st.radio(
        "Variable a comparar con el precio",
        options=["renta_media_hogar", "poblacion_total", "total_vut"],
        format_func=lambda x: {
            "renta_media_hogar": "Renta media del hogar",
            "poblacion_total": "Población total",
            "total_vut": "Nº de viviendas de uso turístico (VUT)",
        }[x],
        horizontal=True,
    )

    # Aggregate by district first, matching the EDA methodology:
    # correlating district-level medians, not individual listings,
    # avoids diluting the signal with within-district price variance.
    district_agg = (
        df_filtered.groupby("neighbourhood_group")
        .agg(price_mediano=("price", "median"), **{variable: (variable, "first")})
        .dropna()
        .reset_index()
    )

    if len(district_agg) < 3:
        st.info("Selecciona al menos 3 distritos en el filtro para calcular la correlación.")
    else:
        fig_scatter = px.scatter(
            district_agg,
            x=variable,
            y="price_mediano",
            text="neighbourhood_group",
            labels={
                "price_mediano": "Precio mediano (€)",
                variable: variable.replace("_", " ").title(),
            },
        )
        fig_scatter.update_traces(textposition="top center")
        st.plotly_chart(fig_scatter, use_container_width=True)

        # --- Statistical test: Pearson correlation (district-level) ---
        corr, p_value = pearsonr(district_agg[variable], district_agg["price_mediano"])

        col1, col2 = st.columns(2)
        col1.metric("Coeficiente de correlación (Pearson)", f"{corr:.2f}")
        col2.metric("p-valor", f"{p_value:.2e}")

        if p_value < 0.05:
            direccion = "positiva" if corr > 0 else "negativa"
            st.success(
                f"La correlación es estadísticamente significativa (p < 0.05). "
                f"Hay evidencia suficiente para afirmar que existe una relación {direccion} "
                f"entre el precio mediano por distrito y esta variable."
            )
        else:
            st.warning(
                "No hay evidencia estadística suficiente (p ≥ 0.05) para afirmar "
                "que existe una relación entre estas dos variables a nivel de distrito."
            )

            