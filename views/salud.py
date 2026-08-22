import streamlit as st

from data_utils import get_df_filtrado, grafico_barras


def render():
    df = get_df_filtrado()

    st.title("Salud")
    st.caption("Cobertura, acceso y dificultades relacionadas con la atención de la salud.")

    col1, col2 = st.columns(2)
    with col1:
        grafico_barras(df, "salud_cobertura", "Cobertura de salud", horizontal=True)
    with col2:
        grafico_barras(df, "metodo_acceso_salud", "Método de acceso a la salud", horizontal=True)

    col3, col4 = st.columns(2)
    with col3:
        grafico_barras(df, "salud_problemas", "Problemas de salud")
    with col4:
        grafico_barras(df, "salud_dificultad_acceso", "Dificultad de acceso a la salud", horizontal=True)

    grafico_barras(df, "tipo_dificultad_salud", "Tipo de dificultad de acceso a la salud", horizontal=True)
