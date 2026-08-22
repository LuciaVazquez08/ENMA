import streamlit as st

from data_utils import get_df_filtrado, grafico_barras


def render():
    df = get_df_filtrado()

    st.title("Trabajo y economía")
    st.caption("Situación ocupacional, circuitos laborales y acceso a ayudas económicas.")

    col1, col2 = st.columns(2)
    with col1:
        grafico_barras(df, "situacion_ocupacional_agrup", "Situación ocupacional", horizontal=True)
    with col2:
        grafico_barras(df, "circuitos_laborales", "Circuitos laborales", horizontal=True)

    col3, col4 = st.columns(2)
    with col3:
        grafico_barras(df, "trabajo_en_area_experiencia", "Trabaja en su área de experiencia")
    with col4:
        grafico_barras(df, "dificultad_trabajo_experiencia", "Dificultad para trabajar en su área")

    grafico_barras(df, "tipo_dificultad_trabajo", "Tipo de dificultad para acceder al trabajo", horizontal=True)

    col5, col6 = st.columns(2)
    with col5:
        grafico_barras(df, "envia_dinero_exterior", "Envía dinero al exterior")
    with col6:
        grafico_barras(df, "recibe_ayuda_economica", "Recibe ayuda económica/alimentaria")
