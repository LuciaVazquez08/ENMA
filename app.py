import pandas as pd
import plotly.express as px
import streamlit as st

from enma_palette import CHART_SEQUENCE, FONT_BODY, inject_fonts

DATA_PATH = "data/processed/ENMA.csv"

st.set_page_config(
    page_title="ENMA - Tablero",
    page_icon="🌎",
    layout="wide",
)
inject_fonts()


@st.cache_data
def cargar_datos(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


df = cargar_datos(DATA_PATH)

st.title("Encuesta Nacional Migrante")
st.markdown(
    "Tablero base para explorar los datos armonizados de las ediciones "
    "**2020** y **2023** de la Encuesta Nacional Migrante (ENMA)."
)

# --- Filtros ---
st.sidebar.header("Filtros")

anios_disponibles = sorted(df["Año"].dropna().unique())
anios = st.sidebar.multiselect("Año de la encuesta", anios_disponibles, default=anios_disponibles)

regiones_disponibles = sorted(df["region"].dropna().unique())
regiones = st.sidebar.multiselect("Región", regiones_disponibles, default=regiones_disponibles)

generos_disponibles = sorted(df["genero_agrup"].dropna().unique())
generos = st.sidebar.multiselect("Género", generos_disponibles, default=generos_disponibles)

df_filtrado = df[
    df["Año"].isin(anios)
    & df["region"].isin(regiones)
    & df["genero_agrup"].isin(generos)
]

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Personas encuestadas", f"{len(df_filtrado):,}".replace(",", "."))
col2.metric("País de nacimiento más frecuente", df_filtrado["pais_nacimiento_var"].mode().iat[0])
col3.metric("Región más representada", df_filtrado["region"].mode().iat[0])
pct_reciente = (df_filtrado["migracion_reciente"] == "si").mean() * 100
col4.metric("Migración reciente (últimos años)", f"{pct_reciente:.1f}%")

st.divider()

# --- Gráficos generales ---
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Distribución por edad")
    edad = df_filtrado["edad_agrupada"].value_counts().sort_index().reset_index()
    edad.columns = ["Rango etario", "Personas"]
    fig_edad = px.bar(edad, x="Rango etario", y="Personas", color_discrete_sequence=CHART_SEQUENCE)
    fig_edad.update_layout(font_family=FONT_BODY)
    st.plotly_chart(fig_edad, use_container_width=True)

with col_der:
    st.subheader("Distribución por género")
    genero = df_filtrado["genero_agrup"].value_counts().reset_index()
    genero.columns = ["Género", "Personas"]
    fig_genero = px.pie(genero, names="Género", values="Personas", color_discrete_sequence=CHART_SEQUENCE, hole=0.45)
    fig_genero.update_layout(font_family=FONT_BODY)
    st.plotly_chart(fig_genero, use_container_width=True)

col_izq2, col_der2 = st.columns(2)

with col_izq2:
    st.subheader("Principales países de nacimiento")
    paises = df_filtrado["pais_nacimiento_var"].value_counts().head(10).sort_values().reset_index()
    paises.columns = ["País", "Personas"]
    fig_paises = px.bar(paises, x="Personas", y="País", orientation="h", color_discrete_sequence=CHART_SEQUENCE)
    fig_paises.update_layout(font_family=FONT_BODY)
    st.plotly_chart(fig_paises, use_container_width=True)

with col_der2:
    st.subheader("Personas encuestadas por región")
    region = df_filtrado["region"].value_counts().reset_index()
    region.columns = ["Región", "Personas"]
    fig_region = px.bar(region, x="Región", y="Personas", color_discrete_sequence=CHART_SEQUENCE)
    fig_region.update_layout(font_family=FONT_BODY)
    st.plotly_chart(fig_region, use_container_width=True)

st.divider()

# --- Datos ---
st.subheader("Explorar los datos")
st.dataframe(df_filtrado, use_container_width=True)
