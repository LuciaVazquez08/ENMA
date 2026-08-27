import pandas as pd
import plotly.express as px
import streamlit as st

from enma_palette import CHART_SEQUENCE, FONT_BODY

DATA_PATH = "data/processed/ENMA.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)

def aplicar_tipografia(fig):
    """DM Sans para todos los textos del gráfico. El título va aparte, vía st.subheader
    (que ya hereda Syncopate del CSS global de la app), no como título nativo de Plotly."""
    fig.update_layout(
        font=dict(family=FONT_BODY),
        legend=dict(font=dict(family=FONT_BODY)),
        hoverlabel=dict(font=dict(family=FONT_BODY)),
    )
    fig.update_xaxes(title_font=dict(family=FONT_BODY), tickfont=dict(family=FONT_BODY))
    fig.update_yaxes(title_font=dict(family=FONT_BODY), tickfont=dict(family=FONT_BODY))
    return fig

def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros")
    contador = st.sidebar.empty()

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

    contador.caption(f"{len(df_filtrado):,}".replace(",", ".") + " personas encuestadas")

    return df_filtrado

def get_df_filtrado() -> pd.DataFrame:
    df_filtrado = st.session_state.get("df_filtrado")
    if df_filtrado is None or df_filtrado.empty:
        st.warning("No hay datos para los filtros seleccionados.")
        st.stop()
    return df_filtrado


def distribucion(df: pd.DataFrame, columna: str, orden: list | None = None) -> pd.DataFrame:
    cantidad = df[columna].dropna().value_counts()
    porcentaje = cantidad.div(cantidad.sum()).mul(100).round(1)
    if orden:
        indice = [c for c in orden if c in cantidad.index]
    else:
        indice = porcentaje.sort_values(ascending=False).index
    data = pd.DataFrame({
        columna: indice,
        "Porcentaje": porcentaje.reindex(indice).values,
        "Cantidad": cantidad.reindex(indice).values,
    })
    return data


def grafico_barras(
    df: pd.DataFrame,
    columna: str,
    titulo: str,
    orden: list | None = None,
    horizontal: bool = False,
    height: int | None = None,
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
            custom_data=["Cantidad"],
        )
        fig.update_layout(yaxis_title=None, xaxis_title="Porcentaje (%)")
        fig.update_xaxes(range=[0, data["Porcentaje"].max() * 1.18])
        hovertemplate = "%{y}<br>Porcentaje: %{x:.1f}%<br>Personas: %{customdata[0]:,.0f}<extra></extra>"
    else:
        fig = px.bar(
            data, x=columna, y="Porcentaje",
            color_discrete_sequence=CHART_SEQUENCE, text="Porcentaje",
            custom_data=["Cantidad"],
        )
        fig.update_layout(xaxis_title=None, yaxis_title="Porcentaje (%)")
        fig.update_yaxes(range=[0, data["Porcentaje"].max() * 1.3])
        hovertemplate = "%{x}<br>Porcentaje: %{y:.1f}%<br>Personas: %{customdata[0]:,.0f}<extra></extra>"
    fig.update_traces(texttemplate="%{text}%", textposition="outside", hovertemplate=hovertemplate)
    fig.update_layout(margin=dict(t=10, b=10))
    aplicar_tipografia(fig)
    if height:
        fig.update_layout(height=height)
    st.plotly_chart(fig, use_container_width=True)
