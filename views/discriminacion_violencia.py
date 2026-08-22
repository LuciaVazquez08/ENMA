import streamlit as st

from data_utils import get_df_filtrado, grafico_barras


def render():
    df = get_df_filtrado()

    st.title("Discriminación y violencia")
    st.caption("Experiencias de discriminación y violencia sufridas por la población migrante encuestada.")

    grafico_barras(df, "discriminacion_experimentada", "Discriminación experimentada")
    grafico_barras(df, "lugar_discriminacion", "Ámbito de la discriminación", horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        grafico_barras(df, "violencia_fuerza_seguridad", "Violencia por parte de fuerzas de seguridad")
    with col2:
        grafico_barras(df, "violencia_genero", "Violencia por razones de género")
