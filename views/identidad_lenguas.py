import plotly.express as px
import streamlit as st

from data_utils import get_df_filtrado, grafico_barras
from enma_palette import CHART_SEQUENCE, FONT_BODY


def _pertenencia_por_pais(df):
    st.subheader("Pertenencia indígena y afrodescendencia")
    sub = df.copy()
    sub["es_indigena"] = sub["descendencia"] == "Descendencia Indígena"
    sub["es_afro"] = sub["descendencia"] == "Afrodescendiente"
    tabla = (
        sub.groupby("pais_nacimiento_var")[["es_indigena", "es_afro"]]
        .mean()
        .mul(100)
        .round(1)
    )
    tabla = tabla.loc[tabla.sum(axis=1).sort_values().index]
    tabla = tabla.rename(columns={"es_indigena": "Pueblos indígenas", "es_afro": "Afrodescendencia"})
    data = tabla.reset_index().melt(
        id_vars="pais_nacimiento_var", var_name="Pertenencia", value_name="Porcentaje"
    )
    fig = px.bar(
        data, x="Porcentaje", y="pais_nacimiento_var", color="Pertenencia",
        orientation="h", barmode="group",
        color_discrete_sequence=CHART_SEQUENCE,
        text="Porcentaje",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(font_family=FONT_BODY, yaxis_title=None, xaxis_title="Porcentaje (%)", margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)


def render():
    df = get_df_filtrado()

    st.title("Identidad y lenguas")
    st.caption("Pertenencia a pueblos indígenas, afrodescendencia y lenguas habladas por la población encuestada.")

    _pertenencia_por_pais(df)
    grafico_barras(df, "idioma_var", "Lenguas habladas", horizontal=True)
