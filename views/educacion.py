import streamlit as st

from data_utils import get_df_filtrado, grafico_barras

NIVEL_EDUCATIVO_ORDEN = [
    "Hasta secundario incompleto",
    "Secundario completo",
    "Superior o universitario completo y más",
    "Prefiero no responder",
]


def render():
    df = get_df_filtrado()

    st.title("Educación")
    st.caption("Nivel educativo alcanzado y situación educativa actual de la población encuestada.")

    grafico_barras(df, "nivel_educativo_agrup", "Nivel educativo", orden=NIVEL_EDUCATIVO_ORDEN)

    col1, col2 = st.columns(2)
    with col1:
        grafico_barras(df, "estudiando_actualmente", "¿Está estudiando actualmente?")
    with col2:
        grafico_barras(df, "tipo_estudio", "Tipo de estudio en curso", horizontal=True)

    grafico_barras(df, "inconveniente_inscripcion_estudio", "Inconvenientes para inscribirse a estudiar", horizontal=True)
