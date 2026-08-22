import plotly.express as px
import streamlit as st

from data_utils import get_df_filtrado, grafico_barras
from enma_palette import CHART_SEQUENCE, FONT_BODY

NIVEL_EDUCATIVO_ORDEN = [
    "Hasta secundario incompleto",
    "Secundario completo",
    "Superior o universitario completo y más",
    "Prefiero no responder",
]

PERIODO_RESIDENCIA_ORDEN = ["Hasta 5 años", "Entre 5 y 9 años", "Más de 10 años"]

ALTURA_GRANDE = 300
ALTURA_CHICA = 180


def _pais_por_genero(df):
    st.subheader("País de origen")
    tabla = df.groupby(["pais_nacimiento", "genero_agrup"]).size().unstack(fill_value=0)
    tabla = tabla.div(tabla.sum(axis=1), axis=0).mul(100).round(1)
    tabla = tabla.loc[tabla.sum(axis=1).sort_values().index]
    data = tabla.reset_index().melt(
        id_vars="pais_nacimiento", var_name="Género", value_name="Porcentaje"
    )
    fig = px.bar(
        data, x="Porcentaje", y="pais_nacimiento", color="Género",
        orientation="h", barmode="stack",
        color_discrete_sequence=CHART_SEQUENCE,
        text="Porcentaje",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="inside")
    fig.update_layout(
        font_family=FONT_BODY, yaxis_title=None, xaxis_title="Porcentaje (%)",
        margin=dict(t=10, b=10), height=ALTURA_GRANDE,
    )
    fig.update_yaxes(tickmode="linear", dtick=1, tickfont=dict(size=9))
    st.plotly_chart(fig, use_container_width=True)


def _pertenencia_por_pais(df):
    st.subheader("Pertenencia indígena y afrodescendencia")
    sub = df.copy()
    sub["Pueblos indígenas"] = sub["descendencia"] == "Descendencia Indígena"
    sub["Afrodescendencia"] = sub["descendencia"] == "Afrodescendiente"
    tabla = sub.groupby("pais_nacimiento")[["Pueblos indígenas", "Afrodescendencia"]].mean().mul(100).round(1)
    tabla = tabla.loc[tabla.sum(axis=1).sort_values().index]
    data = tabla.reset_index().melt(
        id_vars="pais_nacimiento", var_name="Pertenencia", value_name="Porcentaje"
    )
    fig = px.bar(
        data, x="Porcentaje", y="pais_nacimiento", color="Pertenencia",
        orientation="h", barmode="group",
        color_discrete_sequence=CHART_SEQUENCE,
        text="Porcentaje",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(
        font_family=FONT_BODY, yaxis_title=None, xaxis_title="Porcentaje (%)",
        margin=dict(t=10, b=10), height=ALTURA_GRANDE,
    )
    fig.update_xaxes(range=[0, data["Porcentaje"].max() * 1.2])
    fig.update_yaxes(tickmode="linear", dtick=1, tickfont=dict(size=9))
    st.plotly_chart(fig, use_container_width=True)


def _region_por_edad(df):
    st.subheader("Región de residencia")
    tabla = df.groupby(["edad_agrupada", "region"]).size().unstack(fill_value=0)
    tabla = tabla.div(tabla.sum(axis=1), axis=0).mul(100).round(1)
    data = tabla.reset_index().melt(
        id_vars="edad_agrupada", var_name="region", value_name="Porcentaje"
    )
    fig = px.bar(
        data, x="region", y="Porcentaje", color="edad_agrupada",
        barmode="group", color_discrete_sequence=CHART_SEQUENCE,
        text="Porcentaje",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(
        font_family=FONT_BODY, xaxis_title=None, yaxis_title="Porcentaje (%)",
        legend_title="Rango etario", margin=dict(t=10, b=10), height=ALTURA_CHICA,
    )
    st.plotly_chart(fig, use_container_width=True)


def render():
    df = get_df_filtrado()

    st.title("Perfil sociodemográfico")
    st.caption("Composición de la población migrante encuestada según origen, género, descendencia, edad, región y nivel educativo.")

    col1, col2 = st.columns(2)
    with col1:
        _pais_por_genero(df)
    with col2:
        _pertenencia_por_pais(df)

    col3, col4, col5 = st.columns(3)
    with col3:
        _region_por_edad(df)
    with col4:
        grafico_barras(df, "nivel_educativo_agrup", "Nivel educativo", orden=NIVEL_EDUCATIVO_ORDEN, height=ALTURA_CHICA)
    with col5:
        grafico_barras(df, "periodo_residencia", "Años de residencia", orden=PERIODO_RESIDENCIA_ORDEN, height=ALTURA_CHICA)
