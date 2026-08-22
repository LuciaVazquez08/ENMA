import streamlit as st

from data_utils import get_df_filtrado, grafico_barras


def render():
    df = get_df_filtrado()

    st.title("Familia, hogar y vivienda")
    st.caption("Composición del hogar, hijos e hijas, y condiciones de acceso a la vivienda.")

    col1, col2 = st.columns(2)
    with col1:
        grafico_barras(df, "hijos", "Hijos/as", horizontal=True)
    with col2:
        grafico_barras(df, "asistencia_educacion", "Asistencia educativa de hijos/as")

    grafico_barras(df, "inconveniente_educacion", "Inconvenientes en la inscripción educativa", horizontal=True)

    col3, col4 = st.columns(2)
    with col3:
        grafico_barras(df, "hogar_convivencia", "Convivencia en el hogar", horizontal=True)
    with col4:
        grafico_barras(df, "hogar_discapacidad", "Personas con discapacidad en el hogar")

    col5, col6 = st.columns(2)
    with col5:
        grafico_barras(df, "vivienda_tenencia", "Tenencia de la vivienda", horizontal=True)
    with col6:
        grafico_barras(df, "dificultad_vivienda", "Dificultades de acceso a la vivienda", horizontal=True)
