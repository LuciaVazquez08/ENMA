import streamlit as st

from data_utils import get_df_filtrado, grafico_barras


def render():
    df = get_df_filtrado()

    st.title("Participación y percepción")
    st.caption("Participación política y organizativa, y percepción sobre la vida en Argentina.")

    grafico_barras(df, "tipo_participacion_organizacion", "Participación en organizaciones", horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        grafico_barras(df, "voto_elecciones_locales", "Votó en elecciones locales")
    with col2:
        grafico_barras(df, "voto_elecciones_pais_origen", "Votó en elecciones del país de origen")

    col3, col4 = st.columns(2)
    with col3:
        grafico_barras(df, "motivo_no_voto", "Motivo de no voto (local)", horizontal=True)
    with col4:
        grafico_barras(df, "motivo_no_voto_extranjero", "Motivo de no voto (país de origen)", horizontal=True)

    grafico_barras(df, "situacion_vida_argentina", "Percepción sobre su situación de vida en Argentina", horizontal=True)
