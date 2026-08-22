import pandas as pd
import plotly.express as px
import streamlit as st

from enma_palette import CHART_SEQUENCE, FONT_BODY

DATA_PATH = "data/processed/ENMA.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros")

    anios = sorted(df["Año"].dropna().unique())
    sel_anios = st.sidebar.multiselect("Edición / Año", anios, default=anios, key="f_anio")

    nacionalidades = sorted(df["pais_nacimiento_var"].dropna().unique())
    sel_nacionalidades = st.sidebar.multiselect(
        "Nacionalidad", nacionalidades, default=nacionalidades, key="f_nacionalidad"
    )

    generos = sorted(df["genero_agrup"].dropna().unique())
    sel_generos = st.sidebar.multiselect("Género", generos, default=generos, key="f_genero")

    edades = sorted(df["edad_agrupada"].dropna().unique())
    sel_edades = st.sidebar.multiselect("Edades", edades, default=edades, key="f_edad")

    regiones = sorted(df["region"].dropna().unique())
    sel_regiones = st.sidebar.multiselect("Región", regiones, default=regiones, key="f_region")

    df_filtrado = df[
        df["Año"].isin(sel_anios)
        & df["pais_nacimiento_var"].isin(sel_nacionalidades)
        & df["genero_agrup"].isin(sel_generos)
        & df["edad_agrupada"].isin(sel_edades)
        & df["region"].isin(sel_regiones)
    ]

    st.sidebar.caption(f"{len(df_filtrado):,}".replace(",", ".") + " personas encuestadas")

    return df_filtrado


def get_df_filtrado() -> pd.DataFrame:
    df_filtrado = st.session_state.get("df_filtrado")
    if df_filtrado is None or df_filtrado.empty:
        st.warning("No hay datos para los filtros seleccionados.")
        st.stop()
    return df_filtrado


def distribucion(df: pd.DataFrame, columna: str, orden: list | None = None) -> pd.DataFrame:
    conteo = df[columna].dropna().value_counts(normalize=True).mul(100).round(1)
    if orden:
        conteo = conteo.reindex([c for c in orden if c in conteo.index])
    else:
        conteo = conteo.sort_values(ascending=False)
    data = conteo.reset_index()
    data.columns = [columna, "Porcentaje"]
    return data


def grafico_barras(
    df: pd.DataFrame,
    columna: str,
    titulo: str,
    orden: list | None = None,
    horizontal: bool = False,
):
    st.subheader(titulo)
    data = distribucion(df, columna, orden)
    if data.empty:
        st.info("Sin datos para este filtro.")
        return
    if horizontal:
        data = data.iloc[::-1]
        fig = px.bar(
            data, x="Porcentaje", y=columna, orientation="h",
            color_discrete_sequence=CHART_SEQUENCE, text="Porcentaje",
        )
        fig.update_layout(yaxis_title=None, xaxis_title="Porcentaje (%)")
        fig.update_xaxes(range=[0, data["Porcentaje"].max() * 1.18])
    else:
        fig = px.bar(
            data, x=columna, y="Porcentaje",
            color_discrete_sequence=CHART_SEQUENCE, text="Porcentaje",
        )
        fig.update_layout(xaxis_title=None, yaxis_title="Porcentaje (%)")
        fig.update_yaxes(range=[0, data["Porcentaje"].max() * 1.15])
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(font_family=FONT_BODY, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)


def grafico_binarias(df: pd.DataFrame, columnas: dict, titulo: str):
    """columnas: {etiqueta: nombre_columna} de flags 0/1."""
    st.subheader(titulo)
    valores = {
        etiqueta: (df[col].fillna(0).astype(float) == 1).mean() * 100
        for etiqueta, col in columnas.items()
        if col in df.columns
    }
    data = pd.Series(valores).round(1).sort_values(ascending=False).reset_index()
    data.columns = ["Motivo", "Porcentaje"]
    if data.empty:
        st.info("Sin datos para este filtro.")
        return
    fig = px.bar(
        data.iloc[::-1], x="Porcentaje", y="Motivo", orientation="h",
        color_discrete_sequence=CHART_SEQUENCE, text="Porcentaje",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(font_family=FONT_BODY, yaxis_title=None, xaxis_title="Porcentaje (%)", margin=dict(t=10))
    fig.update_xaxes(range=[0, data["Porcentaje"].max() * 1.18])
    st.plotly_chart(fig, use_container_width=True)
