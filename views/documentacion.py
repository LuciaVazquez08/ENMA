import streamlit as st

from data_utils import get_df_filtrado, grafico_barras


def render():
    df = get_df_filtrado()

    st.title("Documentación y asilo")
    st.caption("Situación documentaria, dificultades para tramitar el DNI y solicitudes de asilo o refugio.")

    col1, col2 = st.columns(2)
    with col1:
        grafico_barras(df, "dni_tenencia", "Tenencia de DNI")
    with col2:
        grafico_barras(df, "solicitud_asilo_refugio", "Solicitud de asilo / refugio")

    grafico_barras(df, "dni_dificultad", "Dificultades para tramitar el DNI", horizontal=True)
