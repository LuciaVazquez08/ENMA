import streamlit as st

from data_utils import get_df_filtrado, grafico_barras, grafico_binarias

MOTIVOS = {
    "Estudios / nuevas experiencias": "motivo_estudios_nuevas_experiencias",
    "Mejor trabajo": "motivo_mejor_trabajo",
    "Violencias / persecuciones": "motivo_violencias_persecuciones",
    "Necesidades básicas": "motivo_necesidades_basicas",
    "Motivo familiar": "motivo_familiar",
}

PERIODO_RESIDENCIA_ORDEN = ["Hasta 5 años", "Entre 5 y 9 años", "Más de 10 años"]


def render():
    df = get_df_filtrado()

    st.title("Trayectoria migratoria")
    st.caption("Motivos de la migración, tiempo de residencia y movilidad dentro y fuera del país.")

    grafico_binarias(df, MOTIVOS, "Motivos de la migración")

    col1, col2 = st.columns(2)
    with col1:
        grafico_barras(df, "periodo_residencia", "Años de residencia", orden=PERIODO_RESIDENCIA_ORDEN)
    with col2:
        grafico_barras(df, "migracion_reciente", "Migración reciente (últimos años)")

    col3, col4 = st.columns(2)
    with col3:
        grafico_barras(df, "vivio_otra_provincia", "Vivió antes en otra provincia")
    with col4:
        grafico_barras(df, "mudanza_futura", "Planea mudarse en el futuro")
